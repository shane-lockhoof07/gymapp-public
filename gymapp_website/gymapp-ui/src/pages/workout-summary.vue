<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-btn
                    text
                    @click="$router.push('/workouts')"
                    class="mb-4"
                >
                    <v-icon left>mdi-arrow-left</v-icon>
                    Back to Workouts
                </v-btn>
            </v-col>
        </v-row>
        
        <v-row>
            <v-col cols="12" md="8" offset-md="2">
                <WorkoutSummary
                    :workout-id="workoutId"
                    :show-dismiss="false"
                    :show-edit="true"
                    :show-start-new="true"
                    :is-just-completed="false"
                    @edit="handleEdit"
                    @start-new="handleStartNew"
                />
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import WorkoutSummary from '@/components/WorkoutSummary.vue'
import { useWorkoutStore } from '@/stores/workout'

export default {
    name: 'WorkoutSummaryPage',
    
    components: {
        WorkoutSummary
    },
    
    setup() {
        const workoutStore = useWorkoutStore()
        
        return {
            workoutStore
        }
    },
    
    computed: {
        workoutId() {
            return this.$route.params.id
        }
    },
    
    methods: {
        handleEdit(workout) {
            console.log('Edit workout:', workout)
        },
        
        handleStartNew() {
            this.workoutStore.startWorkout()
            this.$router.push('/workouts')
        }
    }
}
</script>