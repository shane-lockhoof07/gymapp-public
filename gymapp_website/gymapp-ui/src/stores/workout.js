import { defineStore } from 'pinia'
import { useUserStore } from './user'
import { useExerciseStore } from './exercise'
import ApiRequests from '@/api/request'

export const useWorkoutStore = defineStore('workout', {
    state: () => ({
        workouts: [],
        currentWorkout: {
            name: '',
            date: new Date(),
            start_time: null,
            end_time: null,
            exercises: [],
            notes: ''
        },
        loading: false,
        error: null,
        completedWorkoutId: null
    }),

    getters: {
        allWorkouts: (state) => state.workouts,
        
        workoutInProgress: (state) => state.currentWorkout.start_time != null,
        
        currentWorkoutDuration: (state) => {
            if (!state.currentWorkout.start_time) return 0
            const end = state.currentWorkout.end_time || new Date()
            return Math.floor((end - state.currentWorkout.start_time) / 1000 / 60)
        },
        
        currentWorkoutExercises: (state) => [...state.currentWorkout.exercises],
        
        getWorkoutsByDateRange: (state) => (startDate, endDate) => {
            return state.workouts.filter(workout => {
                const workoutDate = new Date(workout.date)
                return workoutDate >= startDate && workoutDate <= endDate
            })
        }
    },

    actions: {
        async initializeWorkoutStore() {
            const userStore = useUserStore()
            
            if (!userStore.isAuthenticated) {
                userStore.initializeAuth()
            }
            
            await new Promise(resolve => setTimeout(resolve, 0))
            
            if (!userStore.currentUser?.item_id) {
                console.error('No user ID found')
                return { success: false, error: 'No user ID found' }
            }
            
            return await this.fetchUserWorkouts(userStore.currentUser.item_id)
        },

        async fetchUserWorkouts(userId) {
            this.loading = true
            this.error = null
            try {
                const response = await ApiRequests.getWorkouts(userId)
                this.workouts = response.data.workouts
                return { success: true, data: this.workouts }
            } catch (error) {
                this.error = error.message
                console.error('Error fetching workouts:', error)
                return { success: false, error: error.message }
            } finally {
                this.loading = false
            }
        },

        startWorkout() {
            this.currentWorkout = {
                name: '',
                date: new Date(),
                start_time: new Date(),
                end_time: null,
                exercises: [],
                notes: ''
            }
            this.completedWorkoutId = null
        },

        addExerciseToWorkout(exercise) {
            this.currentWorkout.exercises.push({
                ...exercise,
                addedAt: new Date()
            })
        },

        updateExerciseInWorkout(index, updatedExercise) {
            if (index >= 0 && index < this.currentWorkout.exercises.length) {
                this.currentWorkout.exercises[index] = {
                    ...updatedExercise,
                    addedAt: this.currentWorkout.exercises[index].addedAt
                }
            }
        },

        removeExerciseFromWorkout(index) {
            if (index >= 0 && index < this.currentWorkout.exercises.length) {
                this.currentWorkout.exercises.splice(index, 1)
            }
        },

        updateWorkoutNotes(notes) {
            this.currentWorkout.notes = notes
        },

        updateWorkoutName(name) {
            this.currentWorkout.name = name
        },

        async finishWorkout() {
            const userStore = useUserStore()
            const exerciseStore = useExerciseStore()
            
            if (!userStore.currentUser?.item_id) {
                throw new Error('No user logged in')
            }

            if (this.currentWorkout.exercises.length === 0) {
                throw new Error('No exercises in workout')
            }

            this.loading = true
            this.error = null

            try {
                this.currentWorkout.end_time = new Date()

                const processedExercises = []
                console.log('Exercise info', this.currentWorkout.exercises)
                for (const exercise of this.currentWorkout.exercises) {
                    console.log('Exercise object', exercise)
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
                    name: this.currentWorkout.name || `Workout - ${new Date().toLocaleDateString()}`,
                    date: this.currentWorkout.date,
                    start_time: this.currentWorkout.start_time,
                    end_time: this.currentWorkout.end_time,
                    workout_list: processedExercises,
                    notes: this.currentWorkout.notes,
                    user_id: userStore.currentUser.item_id
                }

                const response = await ApiRequests.createWorkout(workoutData)
                
                this.workouts.push(response.data)
                
                this.completedWorkoutId = response.data.item_id
                
                this.clearCurrentWorkout()
                
                return { success: true, data: response.data }
                
            } catch (error) {
                this.error = error.message
                console.error('Error finishing workout:', error)
                return { success: false, error: error.message }
            } finally {
                this.loading = false
            }
        },

        clearCurrentWorkout() {
            this.currentWorkout = {
                name: '',
                date: new Date(),
                start_time: null,
                end_time: null,
                exercises: [],
                notes: ''
            }
        },

        getWorkoutStats() {
            const totalWorkouts = this.workouts.length
            const totalExercises = this.workouts.reduce((sum, workout) => 
                sum + (workout.exercises?.length || 0), 0
            )
            
            const avgDuration = this.workouts.reduce((sum, workout) => 
                sum + (workout.duration || 0), 0
            ) / (totalWorkouts || 1)
            
            return {
                totalWorkouts,
                totalExercises,
                avgDuration: Math.round(avgDuration)
            }
        }
    }
})