import axios from "axios";

const API = axios.create({
    baseURL: import.meta.env.VITE_API_URL
})

class ApiRequests {
    static getUsers() {
        return API.get('/usernames');
    }

    static createUser(userData) {
        return API.post('/create', userData);
    }
    
    static loginUser(userData) {
        return API.post('/login', userData);
    }
    
    static updateUser(userId, userData) {
        return API.put(`/users/${userId}`, userData);
    }

    static getExercises() {
        return API.get('/exercises');
    }

    static createExercise(exerciseData) {
        return API.post('/exercises', exerciseData);
    }

    static getWorkouts(userId) {
        return API.get('/workouts', { params: { item_id: userId } });
    }

    static getWorkout(workoutId) {
        return API.get(`/workouts/${workoutId}`);
    }

    static createWorkout(workoutData) {
        return API.post('/workouts', workoutData);
    }

    static updateWorkout(workoutId, workoutData) {
        return API.put(`/workouts/${workoutId}`, workoutData);
    }

    static deleteWorkout(workoutId) {
        return API.delete(`/workouts/${workoutId}`);
    }

    static getPlannedWorkouts(userId) {
        return API.get('/planned-workouts', { params: { user_id: userId } });
    }

    static getPlannedWorkout(workoutId) {
        return API.get(`/planned-workouts/${workoutId}`);
    }

    static createPlannedWorkout(workoutData) {
        return API.post('/planned-workouts', workoutData);
    }

    static updatePlannedWorkout(workoutId, workoutData) {
        return API.put(`/planned-workouts/${workoutId}`, workoutData);
    }

    static deletePlannedWorkout(workoutId) {
        return API.delete(`/planned-workouts/${workoutId}`);
    }
    
    static get(path, config) {
        return API.get(path, config);
    }
    
    static post(path, data, config) {
        return API.post(path, data, config);
    }
    
    static put(path, data, config) {
        return API.put(path, data, config);
    }
    
    static delete(path, config) {
        return API.delete(path, config);
    }
}

export default ApiRequests;