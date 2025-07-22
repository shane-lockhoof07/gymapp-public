import { defineStore } from 'pinia'
import { useUserStore } from './user'
import { useExerciseStore } from './exercise'
import ApiRequests from '@/api/request'

export const usePlannedWorkoutStore = defineStore('plannedWorkout', {
    state: () => ({
        plannedWorkouts: [],
        currentPlannedWorkout: {
            name: '',
            notes: '',
            exercises: []
        },
        selectedPlannedWorkout: null,
        loading: false,
        error: null
    }),

    getters: {
        allPlannedWorkouts: (state) => state.plannedWorkouts,
        
        plannedWorkoutNames: (state) => state.plannedWorkouts.map(workout => ({
            id: workout.item_id,
            name: workout.name,
            notes: workout.notes,
            exerciseCount: workout.exercises?.length || 0
        })),

        getPlannedWorkoutById: (state) => (id) => {
            return state.plannedWorkouts.find(workout => workout.item_id === id)
        }
    },

    actions: {
        async initializePlannedWorkoutStore() {
            const userStore = useUserStore()
            
            if (!userStore.isAuthenticated) {
                userStore.initializeAuth()
            }
            
            if (userStore.currentUser?.item_id) {
                await this.fetchUserPlannedWorkouts(userStore.currentUser.item_id)
            }
        },

        async fetchUserPlannedWorkouts(userId) {
            this.loading = true
            this.error = null
            
            try {
                const response = await ApiRequests.getPlannedWorkouts(userId)
                this.plannedWorkouts = response.data.planned_workouts
                
                return { success: true, data: this.plannedWorkouts }
            } catch (error) {
                this.error = error.message
                console.error('Error fetching planned workouts:', error)
                return { success: false, error: error.message }
            } finally {
                this.loading = false
            }
        },

        async fetchPlannedWorkoutById(workoutId) {
            this.loading = true
            this.error = null
            
            try {
                const response = await ApiRequests.getPlannedWorkout(workoutId)
                this.selectedPlannedWorkout = response.data
                return { success: true, data: response.data }
            } catch (error) {
                this.error = error.message
                console.error('Error fetching planned workout:', error)
                return { success: false, error: error.message }
            } finally {
                this.loading = false
            }
        },

        startPlanningWorkout() {
            this.currentPlannedWorkout = {
                name: '',
                notes: '',
                exercises: []
            }
        },

        addExerciseToPlan(exercise) {
            const exerciseData = {
                ...exercise,
                sets: exercise.sets || [{ weight: '', reps: '' }],
                addedAt: new Date()
            }
            this.currentPlannedWorkout.exercises.push(exerciseData)
        },

        updateExerciseInPlan(index, updatedExercise) {
            if (index >= 0 && index < this.currentPlannedWorkout.exercises.length) {
                this.currentPlannedWorkout.exercises[index] = {
                    ...updatedExercise,
                    addedAt: this.currentPlannedWorkout.exercises[index].addedAt
                }
            }
        },

        removeExerciseFromPlan(index) {
            if (index >= 0 && index < this.currentPlannedWorkout.exercises.length) {
                this.currentPlannedWorkout.exercises.splice(index, 1)
            }
        },

        async savePlannedWorkout() {
            const userStore = useUserStore()
            const exerciseStore = useExerciseStore()
            
            if (!userStore.currentUser?.item_id) {
                throw new Error('No user logged in')
            }

            if (this.currentPlannedWorkout.exercises.length === 0) {
                throw new Error('No exercises in planned workout')
            }

            this.loading = true
            this.error = null

            try {
                const processedExercises = []
                
                for (const exercise of this.currentPlannedWorkout.exercises) {
                    if (!exercise.item_id) {
                        console.log('Creating new exercise:', exercise.name)
                        
                        const exerciseData = {
                            name: exercise.name,
                            description: exercise.description || '',
                            category: exercise.category || 'Strength',
                            equipment: exercise.equipment || 'None',
                            muscles: exercise.muscles || [],
                            sub_muscles: exercise.sub_muscles || []
                        }
                        
                        try {
                            const response = await ApiRequests.createExercise(exerciseData)
                            processedExercises.push({
                                ...exercise,
                                item_id: response.data.item_id,
                                exerciseDetails: response.data
                            })
                            
                            await exerciseStore.fetchExercises()
                        } catch (error) {
                            console.error('Error creating exercise:', error)
                            throw new Error(`Failed to create exercise: ${exercise.name}`)
                        }
                    } else {
                        processedExercises.push(exercise)
                    }
                }

                const workoutData = {
                    name: this.currentPlannedWorkout.name || 'Unnamed Workout Plan',
                    notes: this.currentPlannedWorkout.notes,
                    workout_list: processedExercises,
                    user_id: userStore.currentUser.item_id
                }

                const response = await ApiRequests.createPlannedWorkout(workoutData)
                
                this.plannedWorkouts.push(response.data)
                
                this.clearCurrentPlannedWorkout()
                
                return { success: true, data: response.data }
                
            } catch (error) {
                this.error = error.message
                console.error('Error saving planned workout:', error)
                return { success: false, error: error.message }
            } finally {
                this.loading = false
            }
        },

        loadPlannedWorkoutForTracking(workoutId) {
            console.warn('loadPlannedWorkoutForTracking is deprecated. Use fetchPlannedWorkoutById instead.')
            const plannedWorkout = this.getPlannedWorkoutById(workoutId)
            if (plannedWorkout) {
                return {
                    name: plannedWorkout.name,
                    notes: plannedWorkout.notes,
                    exercises: plannedWorkout.exercise_details || []
                }
            }
            return null
        },

        clearCurrentPlannedWorkout() {
            this.currentPlannedWorkout = {
                name: '',
                notes: '',
                exercises: []
            }
        },

        async deletePlannedWorkout(workoutId) {
            this.loading = true
            this.error = null
            
            try {
                await ApiRequests.deletePlannedWorkout(workoutId)
                
                this.plannedWorkouts = this.plannedWorkouts.filter(
                    workout => workout.item_id !== workoutId
                )
                
                return { success: true }
            } catch (error) {
                this.error = error.message
                console.error('Error deleting planned workout:', error)
                return { success: false, error: error.message }
            } finally {
                this.loading = false
            }
        }
    }
})