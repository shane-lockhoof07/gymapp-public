<template>
    <v-container fluid class="pa-0">
        <v-row>
            <v-col cols="12">
                <!-- Search Bar -->
                <v-text-field
                    v-model="search"
                    prepend-icon="mdi-magnify"
                    label="Search workouts..."
                    single-line
                    hide-details
                    clearable
                    class="mb-4"
                ></v-text-field>
                
                <!-- Workouts List -->
                <v-expansion-panels v-if="paginatedWorkouts.length > 0" v-model="panel">
                    <v-expansion-panel
                        v-for="(workout, index) in paginatedWorkouts"
                        :key="workout.item_id"
                    >
                        <v-expansion-panel-title>
                            <v-row no-gutters align="center">
                                <v-col cols="6">
                                    <span class="text-h6">{{ workout.name || 'Unnamed Workout' }}</span>
                                </v-col>
                                <v-col cols="3" class="text-center">
                                    <v-chip size="small" color="primary">
                                        {{ workout.exercises?.length || 0 }} exercises
                                    </v-chip>
                                </v-col>
                                <v-col cols="3" class="text-right">
                                    <span class="text-caption">{{ formatDate(workout.date) }}</span>
                                </v-col>
                            </v-row>
                        </v-expansion-panel-title>
                        
                        <v-expansion-panel-text>
                            <v-card flat>
                                <v-card-text>
                                    <v-row>
                                        <v-col cols="6">
                                            <strong>Start Time:</strong> {{ formatTime(workout.start_time) }}
                                        </v-col>
                                        <v-col cols="6">
                                            <strong>End Time:</strong> {{ formatTime(workout.end_time) }}
                                        </v-col>
                                    </v-row>
                                    
                                    <v-row v-if="workout.duration">
                                        <v-col>
                                            <strong>Duration:</strong> {{ workout.duration }} minutes
                                        </v-col>
                                    </v-row>
                                    
                                    <v-row v-if="workout.notes">
                                        <v-col>
                                            <strong>Notes:</strong> {{ workout.notes }}
                                        </v-col>
                                    </v-row>
                                    
                                    <v-divider class="my-3"></v-divider>
                                    
                                    <strong>Exercises:</strong>
                                    <v-row class="mt-2">
                                        <v-col>
                                            <div v-if="workout.exercise_performances && workout.exercise_performances.length > 0">
                                                <v-expansion-panels>
                                                    <v-expansion-panel
                                                        v-for="(performance, perfIndex) in workout.exercise_performances.slice(0, 5)"
                                                        :key="perfIndex"
                                                    >
                                                        <v-expansion-panel-title>
                                                            <v-chip
                                                                size="small"
                                                                color="primary"
                                                                class="mr-2"
                                                            >
                                                                {{ getExerciseName(performance.exercise_id) }}
                                                                <span class="ml-1">({{ performance.sets?.length || 0 }} sets)</span>
                                                            </v-chip>
                                                        </v-expansion-panel-title>
                                                        <v-expansion-panel-text>
                                                            <v-simple-table dense v-if="performance.sets?.length">
                                                                <thead>
                                                                    <tr>
                                                                        <th>Set</th>
                                                                        <th>Weight</th>
                                                                        <th>Reps</th>
                                                                    </tr>
                                                                </thead>
                                                                <tbody>
                                                                    <tr v-for="(set, setIdx) in performance.sets" :key="setIdx">
                                                                        <td>{{ setIdx + 1 }}</td>
                                                                        <td>{{ set.weight || 0 }} lbs</td>
                                                                        <td>{{ set.reps || 0 }}</td>
                                                                    </tr>
                                                                </tbody>
                                                            </v-simple-table>
                                                        </v-expansion-panel-text>
                                                    </v-expansion-panel>
                                                </v-expansion-panels>
                                                <span v-if="workout.exercise_performances.length > 5" class="text-caption">
                                                    +{{ workout.exercise_performances.length - 5 }} more exercises
                                                </span>
                                            </div>
                                            <div v-else>
                                                <v-chip
                                                    v-for="(exerciseId, idx) in workout.exercises.slice(0, 5)"
                                                    :key="idx"
                                                    size="small"
                                                    class="mr-1 mb-1"
                                                    color="primary"
                                                >
                                                    {{ getExerciseName(exerciseId) }}
                                                </v-chip>
                                                <span v-if="workout.exercises.length > 5" class="text-caption">
                                                    +{{ workout.exercises.length - 5 }} more
                                                </span>
                                            </div>
                                        </v-col>
                                    </v-row>
                                    
                                    <!-- Quick Stats -->
                                    <v-row class="mt-3" v-if="workout.exercise_performances && workout.exercise_performances.length > 0">
                                        <v-col>
                                            <v-chip size="small" variant="outlined" class="mr-2">
                                                <v-icon start size="small">mdi-dumbbell</v-icon>
                                                Total Sets: {{ getTotalSets(workout) }}
                                            </v-chip>
                                            <v-chip size="small" variant="outlined">
                                                <v-icon start size="small">mdi-weight</v-icon>
                                                Total Volume: {{ getTotalVolume(workout) }} lbs
                                            </v-chip>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                                
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn
                                        text
                                        color="primary"
                                        @click="viewWorkoutSummary(workout.item_id)"
                                    >
                                        View Details
                                        <v-icon end>mdi-arrow-right</v-icon>
                                    </v-btn>
                                    <v-btn
                                        text
                                        @click="duplicateWorkout(workout)"
                                    >
                                        <v-icon start>mdi-content-copy</v-icon>
                                        Duplicate
                                    </v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-expansion-panel-text>
                    </v-expansion-panel>
                </v-expansion-panels>
                
                <!-- Empty State -->
                <v-card v-else flat>
                    <v-card-text class="text-center py-8">
                        <v-icon size="64" color="grey">mdi-history</v-icon>
                        <p class="text-h6 mt-4">{{ search ? 'No workouts found' : 'No previous workouts' }}</p>
                        <p class="text-body-2 text-grey">
                            {{ search ? 'Try adjusting your search' : 'Complete a workout to see it here' }}
                        </p>
                    </v-card-text>
                </v-card>
                
                <!-- Pagination -->
                <v-pagination
                    v-if="totalPages > 1"
                    v-model="currentPage"
                    :length="totalPages"
                    class="mt-4"
                ></v-pagination>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { useWorkoutStore } from '@/stores/workout'
import { useExerciseStore } from '@/stores/exercise'

export default {
    name: 'PreviousWorkouts',
    
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
            panel: [],
            search: '',
            currentPage: 1,
            itemsPerPage: 10
        }
    },
    
    computed: {
        sortedWorkouts() {
            return [...this.workoutStore.workouts].sort((a, b) => {
                const dateA = new Date(a.item_created || a.date)
                const dateB = new Date(b.item_created || b.date)
                return dateB - dateA
            })
        },
        
        filteredWorkouts() {
            if (!this.search) {
                return this.sortedWorkouts
            }
            
            const searchLower = this.search.toLowerCase()
            return this.sortedWorkouts.filter(workout => {
                const nameMatch = workout.name?.toLowerCase().includes(searchLower)
                const dateMatch = this.formatDate(workout.date).toLowerCase().includes(searchLower)
                const exerciseMatch = workout.exercises.some(exerciseId => {
                    const exerciseName = this.getExerciseName(exerciseId)
                    return exerciseName.toLowerCase().includes(searchLower)
                })
                
                return nameMatch || dateMatch || exerciseMatch
            })
        },
        
        paginatedWorkouts() {
            const start = (this.currentPage - 1) * this.itemsPerPage
            const end = start + this.itemsPerPage
            return this.filteredWorkouts.slice(start, end)
        },
        
        totalPages() {
            return Math.ceil(this.filteredWorkouts.length / this.itemsPerPage)
        }
    },
    
    watch: {
        search() {
            this.currentPage = 1
        }
    },
    
    methods: {
        formatDate(dateString) {
            if (!dateString) return 'Unknown Date'
            const date = new Date(dateString)
            return date.toLocaleDateString('en-US', {
                weekday: 'short',
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            })
        },
        
        formatTime(dateString) {
            if (!dateString) return '-'
            const date = new Date(dateString)
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },
        
        getExerciseName(exerciseId) {
            const exercise = this.exerciseStore.exercises.find(e => e.item_id === exerciseId)
            return exercise?.name || 'Unknown'
        },
        
        getTotalSets(workout) {
            if (!workout.exercise_performances) return 0
            return workout.exercise_performances.reduce((total, perf) => 
                total + (perf.sets?.length || 0), 0
            )
        },
        
        getTotalVolume(workout) {
            if (!workout.exercise_performances) return 0
            return workout.exercise_performances.reduce((total, perf) => {
                const setVolume = (perf.sets || []).reduce((setTotal, set) => {
                    const weight = parseFloat(set.weight) || 0
                    const reps = parseFloat(set.reps) || 0
                    return setTotal + (weight * reps)
                }, 0)
                return total + setVolume
            }, 0).toFixed(0)
        },
        
        viewWorkoutSummary(workoutId) {
            this.$router.push(`/workouts/summary/${workoutId}`)
        },
        
        duplicateWorkout(workout) {
            this.workoutStore.startWorkout()
            
            if (workout.exercise_performances && workout.exercise_performances.length > 0) {
                workout.exercise_performances.forEach(performance => {
                    const exercise = this.exerciseStore.exercises.find(e => e.item_id === performance.exercise_id)
                    if (exercise) {
                        this.workoutStore.addExerciseToWorkout({
                            ...exercise,
                            exerciseDetails: exercise,
                            sets: performance.sets?.length > 0 
                                ? performance.sets.map(set => ({ 
                                    weight: set.weight || '', 
                                    reps: set.reps || '' 
                                }))
                                : [{ weight: '', reps: '' }]
                        })
                    }
                })
            } else {
                workout.exercises.forEach(exerciseId => {
                    const exercise = this.exerciseStore.exercises.find(e => e.item_id === exerciseId)
                    if (exercise) {
                        this.workoutStore.addExerciseToWorkout({
                            ...exercise,
                            exerciseDetails: exercise,
                            sets: [{ weight: '', reps: '' }]
                        })
                    }
                })
            }
            
            this.$parent.activeTab = 'current'
            console.log('Workout duplicated with performance data')
        }
    }
}
</script>

<style scoped>
.v-chip {
    font-size: 12px;
}

.v-simple-table {
    margin-top: 8px;
}

.v-expansion-panel-content {
    padding: 8px;
}
</style>