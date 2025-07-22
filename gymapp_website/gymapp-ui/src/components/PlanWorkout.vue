<template>
    <v-container fluid class="pa-0">
        <v-card flat>
            <v-card-text>
                <!-- Workout Name and Notes -->
                <v-row class="mb-4">
                    <v-col cols="12">
                        <v-text-field
                            v-model="plannedWorkoutStore.currentPlannedWorkout.name"
                            label="Workout Plan Name"
                            placeholder="e.g., Upper Body Strength, Leg Day"
                            variant="outlined"
                            density="comfortable"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                        <v-textarea
                            v-model="plannedWorkoutStore.currentPlannedWorkout.notes"
                            label="Workout Notes (optional)"
                            placeholder="Describe the workout goals, intensity, or any special instructions..."
                            variant="outlined"
                            rows="2"
                        ></v-textarea>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col cols="12">
                        <v-btn
                            color="primary"
                            block
                            prepend-icon="mdi-plus"
                            @click="dialog = true"
                        >
                            Add Exercise
                        </v-btn>
                    </v-col>
                </v-row>

                <!-- Current Exercises List -->
                <v-row v-if="plannedWorkoutStore.currentPlannedWorkout.exercises.length > 0">
                    <v-col cols="12">
                        <h3 class="text-h6 mb-3">Planned Exercises</h3>
                        <v-list>
                            <v-list-item
                                v-for="(exercise, index) in plannedWorkoutStore.currentPlannedWorkout.exercises"
                                :key="index"
                                class="px-0"
                            >
                                <v-card variant="outlined" class="mb-2 w-100">
                                    <v-card-text>
                                        <div class="d-flex justify-space-between align-center">
                                            <div>
                                                <h4 class="font-weight-medium">{{ exercise.name }}</h4>
                                                <div class="text-caption text-grey">
                                                    {{ exercise.category }} • {{ exercise.equipment || 'No equipment' }}
                                                </div>
                                                <div class="mt-2">
                                                    <v-chip
                                                        v-for="(set, setIndex) in exercise.sets"
                                                        :key="setIndex"
                                                        size="small"
                                                        class="mr-2"
                                                    >
                                                        Set {{ setIndex + 1 }}: 
                                                        {{ set.weight || '0' }}lbs × {{ set.reps || '0' }} reps
                                                    </v-chip>
                                                </div>
                                            </div>
                                            <div>
                                                <v-btn
                                                    icon="mdi-pencil"
                                                    size="small"
                                                    variant="text"
                                                    @click="editExercise(index)"
                                                ></v-btn>
                                                <v-btn
                                                    icon="mdi-delete"
                                                    size="small"
                                                    variant="text"
                                                    color="error"
                                                    @click="plannedWorkoutStore.removeExerciseFromPlan(index)"
                                                ></v-btn>
                                            </div>
                                        </div>
                                    </v-card-text>
                                </v-card>
                            </v-list-item>
                        </v-list>
                    </v-col>
                </v-row>

                <!-- Empty State -->
                <v-row v-else>
                    <v-col cols="12" class="text-center py-8">
                        <v-icon size="64" color="grey">mdi-dumbbell</v-icon>
                        <p class="text-h6 mt-4 mb-2">No exercises added yet</p>
                        <p class="text-body-2 text-grey">Start adding exercises to your workout plan</p>
                    </v-col>
                </v-row>

                <!-- Save/Cancel Buttons -->
                <v-row class="mt-4" v-if="plannedWorkoutStore.currentPlannedWorkout.exercises.length > 0">
                    <v-col cols="6">
                        <v-btn
                            variant="outlined"
                            block
                            @click="cancelPlanning"
                        >
                            Cancel
                        </v-btn>
                    </v-col>
                    <v-col cols="6">
                        <v-btn
                            color="success"
                            block
                            @click="saveWorkoutPlan"
                            :loading="plannedWorkoutStore.loading"
                            :disabled="!plannedWorkoutStore.currentPlannedWorkout.name"
                        >
                            Save Workout Plan
                        </v-btn>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>

        <!-- Add/Edit Exercise Dialog -->
        <v-dialog v-model="dialog" max-width="600px">
            <v-card>
                <v-card-title>
                    {{ editingIndex !== null ? 'Edit' : 'Add' }} Exercise
                </v-card-title>
                
                <v-card-text>
                    <!-- Exercise Selection -->
                    <v-autocomplete
                        v-model="currentExercise.name"
                        :items="exerciseStore.exerciseNames"
                        label="Exercise"
                        placeholder="Start typing to search exercises..."
                        variant="outlined"
                        clearable
                        :disabled="showNewExerciseForm"
                        @update:model-value="handleExerciseSelect"
                    ></v-autocomplete>
                    
                    <!-- New Exercise Toggle -->
                    <v-checkbox
                        v-model="showNewExerciseForm"
                        label="Create new exercise"
                        @update:model-value="toggleNewExercise"
                    ></v-checkbox>
                    
                    <!-- New Exercise Form -->
                    <v-expand-transition>
                        <div v-if="showNewExerciseForm">
                            <v-text-field
                                v-model="currentExercise.name"
                                label="Exercise Name"
                                variant="outlined"
                                required
                            ></v-text-field>
                            
                            <v-textarea
                                v-model="newExerciseData.description"
                                label="Description"
                                variant="outlined"
                                rows="2"
                            ></v-textarea>
                            
                            <v-select
                                v-model="newExerciseData.category"
                                :items="exerciseStore.categories"
                                label="Category"
                                variant="outlined"
                            ></v-select>
                            
                            <v-select
                                v-model="newExerciseData.equipment"
                                :items="exerciseStore.equipment"
                                label="Equipment"
                                variant="outlined"
                            ></v-select>
                        </div>
                    </v-expand-transition>
                    
                    <!-- Sets Configuration -->
                    <div class="mt-4">
                        <h4 class="mb-2">Sets</h4>
                        <v-row v-for="(set, index) in currentExercise.sets" :key="index" class="mb-2">
                            <v-col cols="5">
                                <v-text-field
                                    v-model="set.weight"
                                    label="Weight (lbs)"
                                    type="number"
                                    variant="outlined"
                                    density="compact"
                                ></v-text-field>
                            </v-col>
                            <v-col cols="5">
                                <v-text-field
                                    v-model="set.reps"
                                    label="Reps"
                                    type="number"
                                    variant="outlined"
                                    density="compact"
                                ></v-text-field>
                            </v-col>
                            <v-col cols="2">
                                <v-btn
                                    icon="mdi-delete"
                                    size="small"
                                    variant="text"
                                    color="error"
                                    @click="removeSet(index)"
                                    :disabled="currentExercise.sets.length === 1"
                                ></v-btn>
                            </v-col>
                        </v-row>
                        
                        <v-btn
                            variant="text"
                            size="small"
                            @click="addSet"
                            prepend-icon="mdi-plus"
                        >
                            Add Set
                        </v-btn>
                    </div>
                </v-card-text>
                
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="closeDialog">Cancel</v-btn>
                    <v-btn
                        color="primary"
                        @click="saveExercise"
                        :disabled="!currentExercise.name"
                    >
                        {{ editingIndex !== null ? 'Update' : 'Add' }} Exercise
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Success Snackbar -->
        <v-snackbar
            v-model="snackbar"
            :timeout="3000"
            color="success"
        >
            Workout plan saved successfully!
        </v-snackbar>
    </v-container>
</template>

<script>
import { useExerciseStore } from '@/stores/exercise'
import { usePlannedWorkoutStore } from '@/stores/plannedWorkout'

export default {
    name: 'PlanWorkout',
    
    setup() {
        const exerciseStore = useExerciseStore()
        const plannedWorkoutStore = usePlannedWorkoutStore()
        
        return {
            exerciseStore,
            plannedWorkoutStore
        }
    },
    
    data() {
        return {
            dialog: false,
            snackbar: false,
            editingIndex: null,
            showNewExerciseForm: false,
            currentExercise: {
                name: '',
                sets: [{ weight: '', reps: '' }]
            },
            newExerciseData: {
                description: '',
                category: '',
                equipment: '',
                muscles: [],
                sub_muscles: []
            }
        }
    },
    
    mounted() {
        this.plannedWorkoutStore.initializePlannedWorkoutStore()
        this.exerciseStore.fetchExercises()
        
        this.plannedWorkoutStore.startPlanningWorkout()
    },
    
    methods: {
        handleExerciseSelect(exerciseName) {
            if (!exerciseName || this.showNewExerciseForm) return
            
            const exercise = this.exerciseStore.getExerciseByName(exerciseName)
            if (exercise) {
                this.currentExercise = {
                    ...exercise,
                    sets: this.currentExercise.sets
                }
            }
        },
        
        toggleNewExercise(value) {
            if (value) {
                this.currentExercise = {
                    name: '',
                    sets: [{ weight: '', reps: '' }]
                }
                this.newExerciseData = {
                    description: '',
                    category: 'Strength',
                    equipment: 'None',
                    muscles: [],
                    sub_muscles: []
                }
            }
        },
        
        addSet() {
            this.currentExercise.sets.push({ weight: '', reps: '' })
        },
        
        removeSet(index) {
            if (this.currentExercise.sets.length > 1) {
                this.currentExercise.sets.splice(index, 1)
            }
        },
        
        editExercise(index) {
            this.editingIndex = index
            const exercise = this.plannedWorkoutStore.currentPlannedWorkout.exercises[index]
            this.currentExercise = {
                ...exercise,
                sets: [...exercise.sets]
            }
            this.dialog = true
        },
        
        saveExercise() {
            const exerciseData = {
                ...this.currentExercise,
                ...this.newExerciseData
            }
            
            if (this.editingIndex !== null) {
                this.plannedWorkoutStore.updateExerciseInPlan(this.editingIndex, exerciseData)
            } else {
                this.plannedWorkoutStore.addExerciseToPlan(exerciseData)
            }
            
            this.closeDialog()
        },
        
        closeDialog() {
            this.dialog = false
            this.editingIndex = null
            this.showNewExerciseForm = false
            this.currentExercise = {
                name: '',
                sets: [{ weight: '', reps: '' }]
            }
            this.newExerciseData = {
                description: '',
                category: '',
                equipment: '',
                muscles: [],
                sub_muscles: []
            }
        },
        
        async saveWorkoutPlan() {
            const result = await this.plannedWorkoutStore.savePlannedWorkout()
            if (result.success) {
                this.snackbar = true
                this.$emit('workout-saved')
                this.plannedWorkoutStore.startPlanningWorkout()
            }
        },
        
        cancelPlanning() {
            if (confirm('Are you sure you want to cancel? All changes will be lost.')) {
                this.plannedWorkoutStore.clearCurrentPlannedWorkout()
                this.plannedWorkoutStore.startPlanningWorkout()
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