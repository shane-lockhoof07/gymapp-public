<template>
    <v-container fluid>
        <v-row>
            <!-- Left Column - Workout Components -->
            <v-col cols="12" md="8">
                <v-card class="mb-4">
                    <v-card-title class="headline">
                        <v-icon left>mdi-dumbbell</v-icon>
                        Workout Center
                    </v-card-title>
                    
                    <v-card-text>
                        <v-tabs v-model="activeTab" class="mb-4">
                            <v-tab value="current">Start Tracking a Workout</v-tab>
                            <v-tab value="planned">Planned Workouts</v-tab>
                            <v-tab value="plan">Plan a Workout</v-tab>
                            <v-tab value="previous">Previous Workouts</v-tab>
                        </v-tabs>
                        
                        <v-row>
                            <v-col cols="12" md="8">
                                <v-tabs-window v-model="activeTab">
                                    <v-tabs-window-item value="current">
                                        <CurrentWorkout 
                                            v-if="!showWorkoutSummary"
                                            @workout-completed="handleWorkoutCompleted"
                                        />
                                        <WorkoutSummary
                                            v-else
                                            :workout-id="completedWorkoutId"
                                            :completed-exercises="completedExercises"
                                            :show-dismiss="true"
                                            :show-edit="false"
                                            :is-just-completed="true"
                                            @dismiss="dismissSummary"
                                            @start-new="startNewWorkout"
                                        />
                                    </v-tabs-window-item>
                                    <v-tabs-window-item value="planned">
                                        <PlannedWorkout />
                                    </v-tabs-window-item>
                                    <v-tabs-window-item value="plan">
                                        <PlanWorkout />
                                    </v-tabs-window-item>
                                    <v-tabs-window-item value="previous">
                                        <PreviousWorkout />
                                    </v-tabs-window-item>
                                </v-tabs-window>
                            </v-col>
                            <v-col cols="12" md="4">
                                <v-card class="mb-4 elevation-0" v-if="workoutStore.workoutInProgress">
                                    <v-card-title>
                                        <v-icon left>mdi-human</v-icon>
                                        Muscle Activation
                                    </v-card-title>
                                    <v-card-text>
                                        <AnatomyHeatmap 
                                            :exercises="workoutStore.currentWorkoutExercises"
                                            @muscle-clicked="handleMuscleClicked"
                                        />
                                    </v-card-text>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
            
            <!-- Right Column - Heatmap and User Info -->
            <v-col cols="12" md="4">                
                <!-- User Info Card -->
                <v-card>
                    <v-card-title>
                        <v-icon left>mdi-account</v-icon>
                        User Profile
                    </v-card-title>
                    <v-card-text>
                        <v-list density="compact">
                            <v-list-item>
                                <v-list-item-title>Username</v-list-item-title>
                                <v-list-item-subtitle>
                                    {{ userStore.currentUser?.username }}
                                </v-list-item-subtitle>
                            </v-list-item>
                            
                            <v-list-item>
                                <v-list-item-title>Member Since</v-list-item-title>
                                <v-list-item-subtitle>
                                    {{ formatDate(userStore.currentUser?.created) }}
                                </v-list-item-subtitle>
                            </v-list-item>
                            
                            <v-list-item>
                                <v-list-item-title>Last Login</v-list-item-title>
                                <v-list-item-subtitle>
                                    {{ formatDate(userStore.currentUser?.last_login) }}
                                </v-list-item-subtitle>
                            </v-list-item>
                            
                            <v-list-item>
                                <v-list-item-title>Experience Level</v-list-item-title>
                                <v-list-item-subtitle>
                                    {{ userStore.currentUser?.experience }} years
                                </v-list-item-subtitle>
                            </v-list-item>
                            
                            <v-divider class="my-2"></v-divider>
                            
                            <!-- Workout Statistics -->
                            <v-list-item>
                                <v-list-item-title>Workout Stats</v-list-item-title>
                            </v-list-item>
                            
                            <v-list-item>
                                <v-list-item-subtitle>
                                    Total Workouts: {{ workoutStats.totalWorkouts }}
                                </v-list-item-subtitle>
                            </v-list-item>
                            
                            <v-list-item>
                                <v-list-item-subtitle>
                                    Avg Duration: {{ workoutStats.avgDuration }}
                                </v-list-item-subtitle>
                            </v-list-item>
                        </v-list>                    
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        
        <!-- Muscle Info Dialog -->
        <v-dialog v-model="muscleDialog" max-width="500">
            <v-card>
                <v-card-title>
                    {{ selectedMuscle?.muscle }} Exercises
                </v-card-title>
                <v-card-text>
                    <div v-if="selectedMuscle">
                        <p>Activation Level: {{ Math.round(selectedMuscle.activation * 100) }}%</p>
                        <p class="mt-2">Exercises targeting this muscle:</p>
                        <ul>
                            <li v-for="(exercise, index) in selectedMuscle.exercises" :key="index">
                                {{ exercise.name }} ({{ exercise.sets?.length || 0 }} sets)
                            </li>
                        </ul>
                    </div>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="muscleDialog = false">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
import { useUserStore } from '@/stores/user'
import { useWorkoutStore } from '@/stores/workout'
import { useExerciseStore } from '@/stores/exercise'
import PlannedWorkout from '@/components/PlannedWorkout.vue'
import CurrentWorkout from '@/components/CurrentWorkout.vue'
import PreviousWorkout from '@/components/PreviousWorkouts.vue'
import AnatomyHeatmap from '@/components/AnatomyHeatmap.vue'
import WorkoutSummary from '@/components/WorkoutSummary.vue'
import PlanWorkout from '@/components/PlanWorkout.vue'

export default {
    name: 'WorkoutLogging',

    components: {
        PlanWorkout,
        PlannedWorkout,
        CurrentWorkout,
        PreviousWorkout,
        AnatomyHeatmap,
        WorkoutSummary
    },
    
    setup() {
        const userStore = useUserStore();
        const workoutStore = useWorkoutStore();
        const exerciseStore = useExerciseStore();

        workoutStore.initializeWorkoutStore();
        exerciseStore.fetchExercises();
        
        return { 
            userStore,
            workoutStore,
            exerciseStore
        }
    },
    
    data() {
        return {
            activeTab: 'current',
            muscleDialog: false,
            selectedMuscle: null,
            showWorkoutSummary: false,
            completedWorkoutId: null,
            completedExercises: null
        }
    },
    
    computed: {
        workoutStats() {
            return this.workoutStore.getWorkoutStats()
        }
    },
    
    async mounted() {
        if (!this.userStore.isLoggedIn) {
            console.log('User not logged in, redirecting...')
            this.$router.push('/')
            return
        }
        
        await this.workoutStore.initializeWorkoutStore()
    },
    
    methods: {
        formatDate(dateString) {
            if (!dateString) return 'Never'
            const date = new Date(dateString)
            return date.toLocaleDateString()
        },
        
        handleMuscleClicked(muscleInfo) {
            this.selectedMuscle = muscleInfo
            this.muscleDialog = true
        },
        
        async handleWorkoutCompleted(workoutData) {
            this.completedWorkoutId = workoutData.item_id
            this.completedExercises = [...this.workoutStore.currentWorkoutExercises]
            
            this.showWorkoutSummary = true
            
            await this.workoutStore.fetchUserWorkouts(this.userStore.currentUser.item_id)
        },
        
        dismissSummary() {
            this.showWorkoutSummary = false
            this.completedWorkoutId = null
            this.completedExercises = null
        },
        
        startNewWorkout() {
            this.showWorkoutSummary = false
            this.completedWorkoutId = null
            this.completedExercises = null
            this.workoutStore.startWorkout();
        }
    }
}
</script>

<style scoped>
.v-tabs {
    margin-bottom: 20px;
}

.v-card {
    margin-bottom: 16px;
}
</style>