<template>
    <v-container fluid class="pa-0">
        <!-- Workout Selection -->
        <v-card flat v-if="!trackingWorkout">
            <v-card-text>
                <h3 class="text-h6 mb-4">Select a Planned Workout</h3>
                
                <!-- Planned Workouts Dropdown -->
                <v-select
                    v-model="selectedWorkoutId"
                    :items="workoutItems"
                    item-title="display"
                    item-value="id"
                    label="Choose a workout plan"
                    variant="outlined"
                    :loading="plannedWorkoutStore.loading"
                    @update:model-value="loadWorkoutDetails"
                >
                    <template v-slot:item="{ props, item }">
                        <v-list-item v-bind="props">
                            <template v-slot:title>
                                <div class="font-weight-medium">{{ item.raw.name }}</div>
                            </template>
                            <template v-slot:subtitle>
                                <div class="text-caption">
                                    {{ item.raw.notes || 'No description' }} • {{ item.raw.exerciseCount }} exercises
                                </div>
                            </template>
                        </v-list-item>
                    </template>
                </v-select>

                <!-- Selected Workout Preview -->
                <v-expand-transition>
                    <v-card v-if="selectedWorkout" variant="outlined" class="mt-4">
                        <v-card-title>{{ selectedWorkout.name }}</v-card-title>
                        <v-card-subtitle v-if="selectedWorkout.notes">
                            {{ selectedWorkout.notes }}
                        </v-card-subtitle>
                        <v-card-text>
                            <h4 class="text-subtitle-2 mb-2">Exercises ({{ selectedWorkout.exercise_details?.length || 0 }})</h4>
                            <v-list density="compact">
                                <v-list-item
                                    v-for="(exercise, index) in selectedWorkout.exercise_details"
                                    :key="index"
                                    class="px-0"
                                >
                                    <v-list-item-title>
                                        {{ index + 1 }}. {{ exercise.name }}
                                    </v-list-item-title>
                                    <v-list-item-subtitle>
                                        {{ exercise.category }} • {{ exercise.equipment || 'No equipment' }}
                                        <span v-if="exercise.sets && exercise.sets.length > 0">
                                            • {{ exercise.sets.length }} sets planned
                                        </span>
                                    </v-list-item-subtitle>
                                </v-list-item>
                            </v-list>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                color="primary"
                                variant="flat"
                                @click="startWorkout"
                                prepend-icon="mdi-play"
                            >
                                Start Workout
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-expand-transition>

                <!-- Empty State -->
                <v-alert
                    v-if="!plannedWorkoutStore.loading && plannedWorkoutStore.plannedWorkouts.length === 0"
                    type="info"
                    variant="tonal"
                    class="mt-4"
                >
                    <div>No planned workouts found. Go to the "Plan a Workout" tab to create your first workout plan!</div>
                </v-alert>
            </v-card-text>
        </v-card>

        <!-- Workout Tracking (Similar to CurrentWorkout) -->
        <div v-else>
            <!-- Workout Header -->
            <v-card flat class="mb-4">
                <v-card-text>
                    <div class="d-flex justify-space-between align-center mb-2">
                        <h3 class="text-h6">{{ currentWorkout.name }}</h3>
                        <v-chip color="primary">
                            <v-icon start>mdi-timer</v-icon>
                            {{ workoutDuration }} min
                        </v-chip>
                    </div>
                    <v-progress-linear
                        :model-value="workoutProgress"
                        height="8"
                        rounded
                        color="success"
                    ></v-progress-linear>
                    <div class="text-caption mt-1">
                        {{ completedExercises }} of {{ totalExercises }} exercises completed
                    </div>
                </v-card-text>
            </v-card>

            <!-- Exercise List -->
            <v-card flat>
                <v-card-text>
                    <h4 class="text-subtitle-1 mb-3">Exercises</h4>
                    <v-list>
                        <v-list-item
                            v-for="(exercise, index) in currentWorkout.exercises"
                            :key="index"
                            class="px-0 mb-2"
                        >
                            <v-card 
                                :variant="exercise.completed ? 'tonal' : 'outlined'"
                                :color="exercise.completed ? 'success' : undefined"
                            >
                                <v-card-text>
                                    <div class="d-flex justify-space-between align-center">
                                        <div class="flex-grow-1">
                                            <h4 class="font-weight-medium">
                                                {{ exercise.name }}
                                                <v-icon v-if="exercise.completed" color="success" size="small" class="ml-1">
                                                    mdi-check-circle
                                                </v-icon>
                                            </h4>
                                            <div class="text-caption text-grey">
                                                {{ exercise.category }} • {{ exercise.equipment || 'No equipment' }}
                                            </div>
                                            <div class="mt-2" v-if="exercise.plannedSets && exercise.plannedSets.length > 0">
                                                <span class="text-caption text-grey">Planned sets:</span>
                                                <v-chip
                                                    v-for="(set, setIndex) in exercise.plannedSets"
                                                    :key="setIndex"
                                                    size="small"
                                                    class="mr-2"
                                                    variant="outlined"
                                                >
                                                    Set {{ setIndex + 1 }}: 
                                                    {{ set.weight || '0' }}lbs × {{ set.reps || '0' }} reps
                                                </v-chip>
                                            </div>
                                            <div class="mt-2" v-if="exercise.sets && exercise.sets.length > 0">
                                                <span class="text-caption text-grey">Completed:</span>
                                                <v-chip
                                                    v-for="(set, setIndex) in exercise.sets"
                                                    :key="setIndex"
                                                    size="small"
                                                    class="mr-2"
                                                    :color="set.completed ? 'success' : 'default'"
                                                    :variant="set.completed ? 'flat' : 'outlined'"
                                                >
                                                    Set {{ setIndex + 1 }}: 
                                                    {{ set.weight || '0' }}lbs × {{ set.reps || '0' }} reps
                                                </v-chip>
                                            </div>
                                        </div>
                                        <v-btn
                                            color="primary"
                                            variant="flat"
                                            size="small"
                                            @click="openExerciseDialog(index)"
                                            :disabled="exercise.completed"
                                        >
                                            {{ exercise.completed ? 'Done' : 'Track' }}
                                        </v-btn>
                                    </div>
                                </v-card-text>
                            </v-card>
                        </v-list-item>
                    </v-list>

                    <!-- Action Buttons -->
                    <v-row class="mt-4">
                        <v-col cols="6">
                            <v-btn
                                variant="outlined"
                                block
                                @click="cancelWorkout"
                            >
                                Cancel Workout
                            </v-btn>
                        </v-col>
                        <v-col cols="6">
                            <v-btn
                                color="success"
                                block
                                @click="finishDialog = true"
                                :disabled="completedExercises === 0"
                            >
                                Finish Workout
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
        </div>

        <!-- Exercise Tracking Dialog -->
        <v-dialog v-model="exerciseDialog" max-width="600px" persistent>
            <v-card>
                <v-card-title>
                    Track: {{ currentExercise.name }}
                </v-card-title>
                
                <v-card-text>
                    <div class="text-body-2 text-grey mb-4">
                        {{ currentExercise.category }} • {{ currentExercise.equipment || 'No equipment' }}
                    </div>
                    
                    <!-- Show planned sets if available -->
                    <div v-if="currentExercise.plannedSets && currentExercise.plannedSets.length > 0" class="mb-4">
                        <h4 class="mb-2">Planned Sets</h4>
                        <v-chip
                            v-for="(set, index) in currentExercise.plannedSets"
                            :key="index"
                            size="small"
                            class="mr-2"
                            color="primary"
                            variant="outlined"
                        >
                            Set {{ index + 1 }}: {{ set.weight || '0' }}lbs × {{ set.reps || '0' }} reps
                        </v-chip>
                    </div>
                    
                    <!-- Sets Tracking -->
                    <div>
                        <h4 class="mb-3">Track Your Sets</h4>
                        <v-row v-for="(set, index) in currentExercise.sets" :key="index" class="mb-3">
                            <v-col cols="1" class="d-flex align-center">
                                <span class="font-weight-bold">{{ index + 1 }}</span>
                            </v-col>
                            <v-col cols="5">
                                <v-text-field
                                    v-model.number="set.weight"
                                    label="Weight (lbs)"
                                    type="number"
                                    variant="outlined"
                                    density="compact"
                                    hide-details
                                ></v-text-field>
                            </v-col>
                            <v-col cols="4">
                                <v-text-field
                                    v-model.number="set.reps"
                                    label="Reps"
                                    type="number"
                                    variant="outlined"
                                    density="compact"
                                    hide-details
                                ></v-text-field>
                            </v-col>
                            <v-col cols="2" class="d-flex align-center">
                                <v-checkbox
                                    v-model="set.completed"
                                    hide-details
                                    density="compact"
                                ></v-checkbox>
                            </v-col>
                        </v-row>
                        
                        <v-btn
                            variant="text"
                            size="small"
                            @click="addSetToExercise"
                            prepend-icon="mdi-plus"
                            class="mt-2"
                        >
                            Add Set
                        </v-btn>
                    </div>
                    
                    <!-- Notes -->
                    <v-textarea
                        v-model="currentExercise.notes"
                        label="Notes (optional)"
                        variant="outlined"
                        rows="2"
                        class="mt-4"
                    ></v-textarea>
                </v-card-text>
                
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="closeExerciseDialog">Cancel</v-btn>
                    <v-btn
                        color="primary"
                        @click="saveExercise"
                    >
                        Save & Continue
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Finish Workout Dialog -->
        <v-dialog v-model="finishDialog" max-width="500px">
            <v-card>
                <v-card-title>Complete Workout</v-card-title>
                <v-card-text>
                    <p class="mb-4">Great job! You've completed {{ completedExercises }} exercises.</p>
                    
                    <v-text-field
                        v-model="workoutName"
                        label="Workout Name"
                        variant="outlined"
                        :placeholder="currentWorkout.name"
                        :rules="[v => !!v || 'Please enter a workout name']"
                    ></v-text-field>
                    
                    <v-textarea
                        v-model="workoutNotes"
                        label="Additional Notes (optional)"
                        placeholder="How did you feel? Any PRs? Notes for next time..."
                        variant="outlined"
                        rows="3"
                    ></v-textarea>
                </v-card-text>
                
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="finishDialog = false">Cancel</v-btn>
                    <v-btn 
                        color="success" 
                        @click="confirmFinishWorkout"
                        :loading="workoutStore.loading"
                        :disabled="!workoutName"
                    >
                        Complete Workout
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
import { useWorkoutStore } from '@/stores/workout'
import { usePlannedWorkoutStore } from '@/stores/plannedWorkout'
import { useExerciseStore } from '@/stores/exercise'

export default {
    name: 'PlannedWorkout',
    
    setup() {
        const workoutStore = useWorkoutStore()
        const plannedWorkoutStore = usePlannedWorkoutStore()
        const exerciseStore = useExerciseStore()
        
        return {
            workoutStore,
            plannedWorkoutStore,
            exerciseStore
        }
    },
    
    data() {
        return {
            selectedWorkoutId: null,
            selectedWorkout: null,
            trackingWorkout: false,
            currentWorkout: {
                name: '',
                exercises: [],
                notes: ''
            },
            exerciseDialog: false,
            finishDialog: false,
            currentExercise: {
                name: '',
                sets: [],
                plannedSets: []
            },
            currentExerciseIndex: null,
            workoutName: '',
            workoutNotes: ''
        }
    },
    
    computed: {
        workoutItems() {
            return this.plannedWorkoutStore.plannedWorkouts.map(workout => ({
                id: workout.item_id,
                name: workout.name,
                notes: workout.notes,
                exerciseCount: workout.exercises?.length || 0,
                display: workout.name
            }))
        },
        
        workoutDuration() {
            return this.workoutStore.currentWorkoutDuration
        },
        
        totalExercises() {
            return this.currentWorkout.exercises.length
        },
        
        completedExercises() {
            return this.currentWorkout.exercises.filter(ex => ex.completed).length
        },
        
        workoutProgress() {
            return this.totalExercises > 0 
                ? (this.completedExercises / this.totalExercises) * 100 
                : 0
        }
    },
    
    async mounted() {
        await this.plannedWorkoutStore.initializePlannedWorkoutStore()
        await this.exerciseStore.fetchExercises()
    },
    
    methods: {
        async loadWorkoutDetails(workoutId) {
            if (workoutId) {
                const result = await this.plannedWorkoutStore.fetchPlannedWorkoutById(workoutId)
                if (result.success) {
                    this.selectedWorkout = result.data
                }
            }
        },
        
        startWorkout() {
            if (!this.selectedWorkout) return
            
            this.workoutStore.startWorkout()
            
            this.currentWorkout = {
                name: this.selectedWorkout.name,
                notes: this.selectedWorkout.notes,
                exercises: this.selectedWorkout.exercise_details.map((exercise, index) => {
                    const plannedSets = exercise.sets || []
                    
                    return {
                        ...exercise,
                        plannedSets: plannedSets,
                        sets: plannedSets.length > 0 
                            ? plannedSets.map(set => ({ weight: '', reps: '', completed: false }))
                            : [{ weight: '', reps: '', completed: false }],
                        completed: false,
                        notes: ''
                    }
                })
            }
            
            this.workoutName = this.selectedWorkout.name
            this.trackingWorkout = true
            
            if (this.currentWorkout.exercises.length > 0) {
                this.openExerciseDialog(0)
            }
        },
        
        openExerciseDialog(index) {
            this.currentExerciseIndex = index
            const exercise = this.currentWorkout.exercises[index]
            
            this.currentExercise = {
                ...exercise,
                sets: [...(exercise.sets || [])],
                plannedSets: [...(exercise.plannedSets || [])]
            }
            
            if (this.currentExercise.plannedSets.length > 0 && this.currentExercise.sets.length === 0) {
                this.currentExercise.sets = this.currentExercise.plannedSets.map(plannedSet => ({
                    weight: plannedSet.weight || '',
                    reps: plannedSet.reps || '',
                    completed: false
                }))
            }
            
            if (this.currentExercise.sets.length === 0) {
                this.currentExercise.sets.push({ weight: '', reps: '', completed: false })
            }
            
            this.exerciseDialog = true
        },
        
        addSetToExercise() {
            this.currentExercise.sets.push({ weight: '', reps: '', completed: false })
        },
        
        saveExercise() {
            this.currentWorkout.exercises[this.currentExerciseIndex] = {
                ...this.currentExercise,
                completed: true
            }
            
            this.workoutStore.addExerciseToWorkout(this.currentExercise)
            
            this.closeExerciseDialog()
            
            const nextIndex = this.currentWorkout.exercises.findIndex(
                (ex, idx) => idx > this.currentExerciseIndex && !ex.completed
            )
            
            if (nextIndex !== -1) {
                setTimeout(() => {
                    this.openExerciseDialog(nextIndex)
                }, 300)
            }
        },
        
        closeExerciseDialog() {
            this.exerciseDialog = false
            this.currentExercise = {
                name: '',
                sets: [],
                plannedSets: []
            }
            this.currentExerciseIndex = null
        },
        
        cancelWorkout() {
            if (confirm('Are you sure you want to cancel this workout? All progress will be lost.')) {
                this.workoutStore.clearCurrentWorkout()
                this.trackingWorkout = false
                this.currentWorkout = {
                    name: '',
                    exercises: [],
                    notes: ''
                }
                this.selectedWorkoutId = null
                this.selectedWorkout = null
            }
        },
        
        async confirmFinishWorkout() {
            this.workoutStore.updateWorkoutName(this.workoutName)
            this.workoutStore.updateWorkoutNotes(this.workoutNotes)
            
            const result = await this.workoutStore.finishWorkout()
            
            if (result.success) {
                this.$emit('workout-completed', result.data)
                this.finishDialog = false
                this.trackingWorkout = false
                this.currentWorkout = {
                    name: '',
                    exercises: [],
                    notes: ''
                }
                this.selectedWorkoutId = null
                this.selectedWorkout = null
            }
        }
    }
}
</script>

<style scoped>
.v-card {
    margin-bottom: 16px;
}
</style>