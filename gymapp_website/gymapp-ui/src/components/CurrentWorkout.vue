<template>
    <v-container fluid>
        <v-row v-if="!workoutStore.workoutInProgress" class="mb-4">
            <v-col>
                <v-btn 
                    color="primary" 
                    size="large" 
                    block
                    @click="startNewWorkout"
                >
                    <v-icon start>mdi-play</v-icon>
                    Start New Workout
                </v-btn>
            </v-col>
        </v-row>

        <!-- Active Workout -->
        <v-row v-if="workoutStore.workoutInProgress" justify="center" align="center">
            <!-- Workout Timer -->
            <v-card class="mb-4 elevation-0">
                <v-card-text class="text-center">
                    <v-icon size="large" color="primary">mdi-timer</v-icon>
                    <h3 class="mt-2">Workout Duration: {{ workoutDuration }} minutes</h3>
                </v-card-text>
            </v-card>

            <!-- Add Exercise Button -->
            <v-btn 
                color="primary" 
                @click="dialog = true" 
                class="mb-4"
                block
            >
                <v-icon start>mdi-plus</v-icon>
                Add Exercise
            </v-btn>

            <!-- Exercise List -->
            <v-row>
                <v-col cols="12">
                    <v-card 
                        outlined 
                        class="pa-4" 
                        style="border-radius: 8px; border-color: white; border-width: 0.25px;background-color: #0f0f0f;"
                        elevation="0"
                        v-if="workoutStore.currentWorkout.exercises.length > 0"
                    >
                        <v-row>
                            <v-col 
                                v-for="(exercise, index) in workoutStore.currentWorkout.exercises" 
                                :key="index"
                                cols="12"
                            >
                            <v-chip
                                class="pa-3 d-flex justify-space-between align-center"
                                rounded="xl"
                                outlined
                                style="height: auto; white-space: normal; width: 100%;"
                                >
                                <div @click="editExercise(index)" style="flex: 1 1 auto; cursor: pointer;">
                                    <div class="font-weight-bold mb-1">{{ exercise.name }}</div>
                                    <div class="text-caption">{{ formatSets(exercise.sets) }}</div>
                                </div>
                                <v-btn
                                    icon
                                    variant="text"
                                    @click.stop="removeExercise(index)" 
                                    style="height: 100%; position: absolute; right: 0; top: 0; bottom: 0; border-radius: 4px;"
                                >
                                    <v-icon>mdi-delete</v-icon>
                                </v-btn>
                            </v-chip>
                            </v-col>
                        </v-row>
                    </v-card>
                </v-col>
            </v-row>

            <!-- Finish Workout Button -->
            <v-btn 
                color="success" 
                size="large" 
                block 
                @click="finishDialog = true"
                class="mt-4"
            >
                <v-icon start>mdi-check</v-icon>
                Finish Workout
            </v-btn>
        </v-row>

        <!-- Add/Edit Exercise Dialog -->
        <v-dialog v-model="dialog" max-width="600px">
            <v-card>
                <v-card-title>
                    {{ editingIndex !== null ? 'Edit Exercise' : 'Add Exercise' }}
                </v-card-title>
                
                <v-card-text>
                    <v-row>
                        <v-col cols="12">
                            <v-combobox
                                v-model="currentExercise.name"
                                :items="exerciseStore.exerciseNames"
                                label="Exercise Name"
                                @update:model-value="onExerciseChange"
                                clearable
                                :return-object="false"
                            ></v-combobox>
                        </v-col>
                    </v-row>
                    <v-expand-transition>
                        <div v-if="showNewExerciseForm">
                            <v-text-field
                                v-model="currentExercise.name"
                                label="Exercise Name"
                                required
                            ></v-text-field>
                            
                            <v-textarea
                                v-model="newExerciseData.description"
                                label="Description"
                                rows="2"
                            ></v-textarea>
                            
                            <v-select
                                v-model="newExerciseData.category"
                                :items="['Strength', 'Cardio', 'Flexibility', 'Balance']"
                                label="Category"
                            ></v-select>
                            
                            <v-select
                                v-model="newExerciseData.equipment"
                                :items="exerciseStore.equipmentOptions"
                                label="Equipment"
                            ></v-select>
                            
                            <v-select
                                v-model="newExerciseData.muscles"
                                :items="exerciseStore.muscleOptions"
                                label="Primary Muscles"
                                multiple
                                chips
                            ></v-select>
                            
                            <v-select
                                v-model="newExerciseData.sub_muscles"
                                :items="exerciseStore.muscleOptions"
                                label="Secondary Muscles"
                                multiple
                                chips
                            ></v-select>
                        </div>
                    </v-expand-transition>
                    
                    <!-- Sets -->
                    <v-row>
                        <v-col cols="12">
                            <span class="text-subtitle-1">Sets</span>
                        </v-col>
                    </v-row>
                    <v-row 
                        v-for="(set, setIndex) in currentExercise.sets" 
                        :key="setIndex"
                        class="align-center"
                    >
                        <v-col cols="5">
                            <v-text-field
                                v-model.number="set.weight"
                                label="Weight"
                                type="number"
                                suffix="lbs"
                                dense
                                @input="checkAutoAddSet(setIndex)"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="5">
                            <v-text-field
                                v-model.number="set.reps"
                                label="Reps"
                                type="number"
                                dense
                                @input="checkAutoAddSet(setIndex)"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="2">
                            <v-btn
                                icon
                                small
                                color="error"
                                @click="removeSet(setIndex)"
                                :disabled="currentExercise.sets.length === 1"
                            >
                                <v-icon small>mdi-delete</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card-text>
                
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="closeDialog">Cancel</v-btn>
                    <v-btn 
                        color="primary" 
                        @click="saveExercise"
                        :disabled="!currentExercise.name || currentExercise.sets.length === 0"
                    >
                        Save
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Finish Workout Dialog -->
        <v-dialog v-model="finishDialog" max-width="500px">
            <v-card>
                <v-card-title>Complete Workout</v-card-title>
                
                <v-card-text>
                    <v-text-field
                        v-model="workoutName"
                        label="Workout Name"
                        :placeholder="`Workout - ${new Date().toLocaleDateString()}`"
                        :rules="[v => !!v || 'Please enter a workout name']"
                    ></v-text-field>
                    
                    <v-textarea
                        v-model="workoutStore.currentWorkout.notes"
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
import { useUserStore } from '@/stores/user'
import { useExerciseStore } from '@/stores/exercise'
import { useWorkoutStore } from '@/stores/workout'

export default {
    name: 'CurrentWorkout',
    
    setup() {
        const userStore = useUserStore()
        const exerciseStore = useExerciseStore()
        const workoutStore = useWorkoutStore()
        
        return {
            userStore,
            exerciseStore,
            workoutStore
        }
    },
    
    data() {
        return {
            dialog: false,
            finishDialog: false,
            workoutName: '',
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
    
    computed: {
        workoutDuration() {
            return this.workoutStore.currentWorkoutDuration
        },

        isNewExercise() {
            return this.currentExercise.name && 
                   !this.exerciseStore.exerciseNames.includes(this.currentExercise.name);
        },
    },
    
    methods: {
        startNewWorkout() {
            console.log('Starting new workout...')
            this.workoutStore.startWorkout()
        },
                
        addSet() {
            this.currentExercise.sets.push({ weight: '', reps: '' })
        },
        
        removeSet(exerciseIndex, setIndex) {
            this.workoutStore.currentWorkout.exercises[exerciseIndex].sets.splice(setIndex, 1)
        },
        
        saveExercise() {
            if (this.showNewExerciseForm) {
                this.currentExercise = {
                    ...this.currentExercise,
                    ...this.newExerciseData,
                    isNew: true
                }
            } else {
                console.log((this.exerciseStore.exercises.find(ex => ex.name === this.currentExercise.name) || {}).item_id)
                this.currentExercise.item_id = (this.exerciseStore.exercises.find(ex => ex.name === this.currentExercise.name) || {}).item_id;
            }
            
            if (this.editingIndex !== null) {
                this.workoutStore.updateExerciseInWorkout(this.editingIndex, this.currentExercise)
            } else {
                this.workoutStore.addExerciseToWorkout(this.currentExercise)
            }
            
            this.closeDialog()
        },
        
        editExercise(index) {
            this.editingIndex = index
            this.currentExercise = JSON.parse(JSON.stringify(this.workoutStore.currentWorkout.exercises[index]))
            this.dialog = true
        },
        
        removeExercise(index) {
            this.workoutStore.removeExerciseFromWorkout(index)
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

        onExerciseChange(value) {
            if (!this.isNewExercise) {
                this.newExerciseData = {
                    description: '',
                    category: '',
                    equipment: '',
                    muscles: [],
                    sub_muscles: []
                };
            } 
        },

        formatSets(sets) {
            return sets
                .filter(set => set.weight !== '' || set.reps !== '')
                .map(set => `${set.weight} x ${set.reps}`)
                .join(', ');
        },

        checkAutoAddSet(index) {
            if (index === this.currentExercise.sets.length - 1) {
                const currentSet = this.currentExercise.sets[index];
                if (currentSet.weight && currentSet.reps) {
                    this.currentExercise.sets.push({ weight: '', reps: '' });
                }
            }
        },

        removeSet(index) {
            if (this.currentExercise.sets.length > 1) {
                this.currentExercise.sets.splice(index, 1);
            }
        },
        
        async confirmFinishWorkout() {
            this.workoutStore.currentWorkout.name = this.workoutName
            const result = await this.workoutStore.finishWorkout()
            
            if (result.success) {
                this.$emit('workout-completed')
                this.finishDialog = false
                this.workoutName = ''
            } else {
                console.error('Failed to complete workout:', result.error)
            }
        }
    }
}
</script>

<style scoped>
.v-chip {
    font-size: 12px;
}
</style>