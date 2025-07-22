import { defineStore } from 'pinia'
import ApiRequests from '@/api/request'

export const useExerciseStore = defineStore('exercise', {
    state: () => ({
        exercises: [],
        categories: [],
        equipment: [],
        loading: false,
        error: null,
        newExercises: []
    }),

    getters: {
        allExercises: (state) => state.exercises,
        exerciseNames: (state) => state.exercises.map(ex => ex.name),
        getExerciseByName: (state) => (name) => {
            return state.exercises.find(ex => ex.name === name)
        },
        allCategories: (state) => state.categories,
        allEquipment: (state) => state.equipment
    },

    actions: {
        async fetchExercises() {
            this.loading = true
            this.error = null
            try {
                const response = await ApiRequests.getExercises()
                this.exercises = response.data.exercises
                this.categories = response.data.categories.filter(cat => cat !== null)
                this.equipment = response.data.equipment.filter(eq => eq !== null)
                return { success: true, data: this.exercises }
            } catch (error) {
                this.error = error.message
                return { success: false, error: error.message }
            } finally {
                this.loading = false
            }
        },

        addNewExercise(exerciseData) {
            const newExercise = {
                ...exerciseData,
                isNew: true,
                tempId: Date.now()
            }
            this.newExercises.push(newExercise)
            this.exercises.push(newExercise)
        },

        async saveNewExercises() {
            const results = []
            for (const exercise of this.newExercises) {
                try {
                    const { isNew, tempId, ...exerciseData } = exercise
                    const response = await ApiRequests.createExercise(exerciseData)
                    const index = this.exercises.findIndex(ex => ex.tempId === tempId)
                    if (index !== -1) {
                        this.exercises[index] = response.data
                    }
                    results.push({ success: true, data: response.data })
                } catch (error) {
                    results.push({ success: false, error: error.message, exercise })
                }
            }
            this.newExercises = []
            return results
        }
    }
})