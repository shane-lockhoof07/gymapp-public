<template>
    <v-card class="workout-summary">
        <v-card-title class="text-h4 text-center">
            <v-icon left large color="success">mdi-check-circle</v-icon>
            {{ isJustCompleted ? 'Workout Complete!' : workout?.name || 'Workout Summary' }}
        </v-card-title>
        
        <v-card-text v-if="workout">
            <!-- Summary Stats -->
            <v-row class="text-center mb-4">
                <v-col cols="4">
                    <div class="text-h3 primary--text">{{ exerciseCount }}</div>
                    <div class="text-subtitle-1">Exercises</div>
                </v-col>
                <v-col cols="4">
                    <div class="text-h3 primary--text">{{ totalSets }}</div>
                    <div class="text-subtitle-1">Total Sets</div>
                </v-col>
                <v-col cols="4">
                    <div class="text-h3 primary--text">{{ workout.duration || 0 }}</div>
                    <div class="text-subtitle-1">Minutes</div>
                </v-col>
            </v-row>
            
            <v-divider class="mb-4"></v-divider>
            
            <!-- Workout Details -->
            <v-row>
                <v-col cols="12" md="6">
                    <div class="mb-3">
                        <strong>Date:</strong> {{ formatDate(workout.date) }}
                    </div>
                    <div class="mb-3">
                        <strong>Time:</strong> {{ formatTime(workout.start_time) }} - {{ formatTime(workout.end_time) }}
                    </div>
                </v-col>
                <v-col cols="12" md="6">
                    <div class="mb-3">
                        <strong>Workout Name:</strong> {{ workout.name || 'Unnamed Workout' }}
                    </div>
                    <div class="mb-3">
                        <strong>Total Volume:</strong> {{ totalVolume }} lbs
                    </div>
                </v-col>
            </v-row>
            
            <div v-if="workout.notes" class="mb-4">
                <strong>Notes:</strong>
                <p class="mt-1">{{ workout.notes }}</p>
            </div>
            
            <!-- Exercise List -->
            <h3 class="mb-3">Exercises Performed</h3>
            <v-expansion-panels v-if="exercisePerformances.length">
                <v-expansion-panel
                    v-for="(performance, index) in exercisePerformances"
                    :key="index"
                >
                    <v-expansion-panel-header>
                        <div>
                            <strong>{{ getExerciseName(performance.exercise_id) }}</strong>
                            <span class="ml-2 text-caption">
                                ({{ performance.sets?.length || 0 }} sets)
                            </span>
                        </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <v-simple-table dense v-if="performance.sets?.length">
                            <thead>
                                <tr>
                                    <th>Set</th>
                                    <th>Weight (lbs)</th>
                                    <th>Reps</th>
                                    <th>Volume</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(set, setIndex) in performance.sets" :key="setIndex">
                                    <td>{{ setIndex + 1 }}</td>
                                    <td>{{ set.weight || 0 }}</td>
                                    <td>{{ set.reps || 0 }}</td>
                                    <td>{{ (set.weight || 0) * (set.reps || 0) }} lbs</td>
                                </tr>
                                <tr class="font-weight-bold">
                                    <td colspan="3">Total</td>
                                    <td>{{ getExerciseVolume(performance) }} lbs</td>
                                </tr>
                            </tbody>
                        </v-simple-table>
                        
                        <div class="mt-2" v-if="getExerciseDetails(performance.exercise_id)">
                            <v-chip 
                                v-for="muscle in getExerciseDetails(performance.exercise_id).muscles" 
                                :key="muscle"
                                small
                                class="mr-1 mb-1"
                                color="primary"
                            >
                                {{ muscle }}
                            </v-chip>
                            <v-chip 
                                v-for="muscle in getExerciseDetails(performance.exercise_id).sub_muscles" 
                                :key="muscle"
                                small
                                class="mr-1 mb-1"
                                outlined
                            >
                                {{ muscle }}
                            </v-chip>
                        </div>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
            
            <!-- Fallback for just completed workouts using detailedExercises -->
            <v-expansion-panels v-else-if="detailedExercises.length">
                <v-expansion-panel
                    v-for="(exercise, index) in detailedExercises"
                    :key="index"
                >
                    <v-expansion-panel-header>
                        <div>
                            <strong>{{ exercise.name }}</strong>
                            <span class="ml-2 text-caption">
                                ({{ exercise.sets?.length || 0 }} sets)
                            </span>
                        </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <v-simple-table dense v-if="exercise.sets?.length">
                            <thead>
                                <tr>
                                    <th>Set</th>
                                    <th>Weight (lbs)</th>
                                    <th>Reps</th>
                                    <th>Volume</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(set, setIndex) in exercise.sets" :key="setIndex">
                                    <td>{{ setIndex + 1 }}</td>
                                    <td>{{ set.weight || 0 }}</td>
                                    <td>{{ set.reps || 0 }}</td>
                                    <td>{{ (set.weight || 0) * (set.reps || 0) }} lbs</td>
                                </tr>
                            </tbody>
                        </v-simple-table>
                        
                        <div class="mt-2">
                            <v-chip 
                                v-for="muscle in exercise.exerciseDetails?.muscles" 
                                :key="muscle"
                                small
                                class="mr-1 mb-1"
                                color="primary"
                            >
                                {{ muscle }}
                            </v-chip>
                            <v-chip 
                                v-for="muscle in exercise.exerciseDetails?.sub_muscles" 
                                :key="muscle"
                                small
                                class="mr-1 mb-1"
                                outlined
                            >
                                {{ muscle }}
                            </v-chip>
                        </div>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
            
            <!-- Muscle Activation Summary -->
            <div class="mt-4">
                <h3 class="mb-3">Muscles Worked</h3>
                <v-chip-group>
                    <v-chip 
                        v-for="muscle in musclesWorked" 
                        :key="muscle"
                        color="primary"
                        outlined
                    >
                        {{ muscle }}
                    </v-chip>
                </v-chip-group>
            </div>
        </v-card-text>
        
        <v-card-text v-else class="text-center">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <p class="mt-2">Loading workout data...</p>
        </v-card-text>
        
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn 
                v-if="showDismiss"
                text 
                @click="$emit('dismiss')"
            >
                Dismiss
            </v-btn>
            <v-btn 
                v-if="showEdit"
                text
                @click="editWorkout"
            >
                Edit Workout
            </v-btn>
            <v-btn 
                v-if="showStartNew"
                color="primary"
                @click="startNewWorkout"
            >
                Start New Workout
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
import { useWorkoutStore } from '@/stores/workout'
import { useExerciseStore } from '@/stores/exercise'
import ApiRequests from '@/api/request'

export default {
    name: 'WorkoutSummary',
    
    props: {
        workoutId: {
            type: String,
            default: null
        },
        showDismiss: {
            type: Boolean,
            default: false
        },
        showEdit: {
            type: Boolean,
            default: true
        },
        showStartNew: {
            type: Boolean,
            default: true
        },
        isJustCompleted: {
            type: Boolean,
            default: false
        },
        completedExercises: {
            type: Array,
            default: null
        }
    },
    
    emits: ['dismiss', 'edit', 'start-new'],
    
    setup() {
        const workoutStore = useWorkoutStore()
        const exerciseStore = useExerciseStore()
        
        return {
            workoutStore,
            exerciseStore
        }
    },
    
    data() {
        return {
            workout: null,
            detailedExercises: [],
            exercisePerformances: []
        }
    },
    
    computed: {
        exerciseCount() {
            if (this.completedExercises) {
                return this.completedExercises.length
            }
            return this.workout?.exercises?.length || 0
        },
        
        totalSets() {
            if (this.exercisePerformances.length) {
                return this.exercisePerformances.reduce((total, perf) => 
                    total + (perf.sets?.length || 0), 0
                )
            }
            if (this.completedExercises) {
                return this.completedExercises.reduce((total, exercise) => 
                    total + (exercise.sets?.length || 0), 0
                )
            }
            if (this.detailedExercises.length) {
                return this.detailedExercises.reduce((total, exercise) => 
                    total + (exercise.sets?.length || 0), 0
                )
            }
            return 0
        },
        
        totalVolume() {
            let volume = 0
            
            if (this.exercisePerformances.length) {
                volume = this.exercisePerformances.reduce((total, perf) => {
                    return total + this.getExerciseVolume(perf)
                }, 0)
            } else if (this.completedExercises) {
                volume = this.completedExercises.reduce((total, exercise) => {
                    const exerciseVolume = (exercise.sets || []).reduce((setTotal, set) => {
                        return setTotal + ((parseFloat(set.weight) || 0) * (parseFloat(set.reps) || 0))
                    }, 0)
                    return total + exerciseVolume
                }, 0)
            }
            
            return volume.toFixed(0)
        },
        
        musclesWorked() {
            const muscles = new Set()
            
            if (this.completedExercises) {
                this.completedExercises.forEach(exercise => {
                    exercise.exerciseDetails?.muscles?.forEach(m => muscles.add(m))
                    exercise.exerciseDetails?.sub_muscles?.forEach(m => muscles.add(m))
                })
            } else if (this.workout?.exercises) {
                this.workout.exercises.forEach(exerciseId => {
                    const exercise = this.exerciseStore.exercises.find(e => e.item_id === exerciseId)
                    if (exercise) {
                        exercise.muscles?.forEach(m => muscles.add(m))
                        exercise.sub_muscles?.forEach(m => muscles.add(m))
                    }
                })
            }
            
            return Array.from(muscles)
        }
    },
    
    watch: {
        workoutId() {
            this.loadWorkout()
        }
    },
    
    mounted() {
        this.loadWorkout()
    },
    
    methods: {
        formatDate(dateString) {
            const date = new Date(dateString)
            return date.toLocaleDateString()
        },
        
        formatTime(dateString) {
            if (!dateString) return '-'
            const date = new Date(dateString)
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },
        
        getExerciseName(exerciseId) {
            const exercise = this.exerciseStore.exercises.find(e => e.item_id === exerciseId)
            return exercise?.name || 'Unknown Exercise'
        },
        
        getExerciseDetails(exerciseId) {
            return this.exerciseStore.exercises.find(e => e.item_id === exerciseId)
        },
        
        getExerciseVolume(performance) {
            return (performance.sets || []).reduce((total, set) => {
                return total + ((parseFloat(set.weight) || 0) * (parseFloat(set.reps) || 0))
            }, 0)
        },
        
        editWorkout() {
            this.$emit('edit', this.workout)
        },
        
        startNewWorkout() {
            this.workoutStore.startWorkout()
            this.$emit('start-new')
        },
        
        async loadWorkout() {
            if (this.workoutId) {
                try {
                    const response = await ApiRequests.get(`/workouts/${this.workoutId}`)
                    const workoutData = response.data
                    
                    this.workout = workoutData
                    this.exercisePerformances = workoutData.exercise_performances || []
                    this.detailedExercises = workoutData.detailed_exercises || []
                    
                } catch (error) {
                    console.error('Error fetching workout details:', error)
                    this.workout = this.workoutStore.workouts.find(w => w.item_id === this.workoutId)
                    if (this.workout) {
                        this.exercisePerformances = this.workout.exercise_performances || []
                    }
                }
            }
            
            if (this.completedExercises) {
                this.detailedExercises = this.completedExercises
            }
            
            if (!this.exerciseStore.exercises.length) {
                await this.exerciseStore.fetchExercises()
            }
        }
    }
}
</script>

<style scoped>
.workout-summary {
    width: 100%;
}

.v-expansion-panel-content {
    padding: 16px;
}

.v-chip {
    margin-bottom: 4px;
}
</style>