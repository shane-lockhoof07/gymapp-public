<template>
    <div class="muscle-heatmap">
        <svg viewBox="0 0 400 600" xmlns="http://www.w3.org/2000/svg">
            <!-- Front View -->
            <g v-if="view === 'front'">
                <!-- Muscle Groups -->
                <!-- Chest (wider shape with rounded edges) -->
                <path 
                    id="chest"
                    d="M 110 120 Q 110 90 155 90 L 245 90 Q 290 90 290 120 L 290 135 Q 290 165 245 165 L 155 165 Q 110 165 110 135 Z"
                    :fill="getHeatColor('Chest')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Chest')"
                    @mouseleave="hideTooltip"
                />
                
                <!-- Shoulders (rounded shapes) -->
                <path 
                    id="shoulders-left"
                    d="M 120 115 Q 120 110 125 110 L 145 110 Q 150 110 150 115 L 150 135 Q 150 140 145 140 L 125 140 Q 120 140 120 135 Z"
                    :fill="getHeatColor('Shoulders')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Shoulders')"
                    @mouseleave="hideTooltip"
                />
                <path 
                    id="shoulders-right"
                    d="M 250 115 Q 250 110 255 110 L 275 110 Q 280 110 280 115 L 280 135 Q 280 140 275 140 L 255 140 Q 250 140 250 135 Z"
                    :fill="getHeatColor('Shoulders')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Shoulders')"
                    @mouseleave="hideTooltip"
                />
                
                <!-- Biceps (larger curved shapes) -->
                <path 
                    id="biceps-left"
                    d="M 115 145 Q 125 140 135 145 L 135 200 Q 125 205 115 200 Z"
                    :fill="getHeatColor('Biceps')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Biceps')"
                    @mouseleave="hideTooltip"
                />
                <path 
                    id="biceps-right"
                    d="M 265 145 Q 275 140 285 145 L 285 200 Q 275 205 265 200 Z"
                    :fill="getHeatColor('Biceps')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Biceps')"
                    @mouseleave="hideTooltip"
                />
                
                <!-- Core/Abs (segmented sections with rounded edges) -->
                <path 
                    id="core-upper"
                    d="M 130 180 Q 130 175 155 175 L 245 175 Q 270 175 270 180 L 250 285 Q 250 290 230 290 L 170 290 Q 175 290 150 285 Z"
                    :fill="getHeatColor('Core')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Core')"
                    @mouseleave="hideTooltip"
                />                
                <!-- Quadriceps (curved muscle shapes) -->
                <path 
                    id="quads-left"
                    d="M 140 300 Q 140 295 145 295 L 175 295 Q 180 295 180 300 L 180 390 Q 180 395 175 395 L 145 395 Q 140 395 140 390 Z"
                    :fill="getHeatColor('Quadriceps')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Quadriceps')"
                    @mouseleave="hideTooltip"
                />
                <path 
                    id="quads-right"
                    d="M 220 300 Q 220 295 225 295 L 255 295 Q 260 295 260 300 L 260 390 Q 260 395 255 395 L 225 395 Q 220 395 220 390 Z"
                    :fill="getHeatColor('Quadriceps')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Quadriceps')"
                    @mouseleave="hideTooltip"
                />
            </g>
            
            <!-- Back View -->
            <g v-else>
                <!-- Traps (two separate shapes with angled tops) -->
                <path 
                    id="traps-left"
                    d="M 110 90 L 170 80 L 170 120 L 110 120 Z"
                    :fill="getHeatColor('Traps')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Traps')"
                    @mouseleave="hideTooltip"
                />
                <path 
                    id="traps-right"
                    d="M 230 80 L 290 90 L 290 120 L 230 120 Z"
                    :fill="getHeatColor('Traps')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Traps')"
                    @mouseleave="hideTooltip"
                />
                
                <!-- Shoulders (rounded rectangles on outer edges) -->
                <path 
                    id="shoulders-left-back"
                    d="M 70 95 Q 70 90 75 90 L 95 90 Q 100 90 100 95 L 100 125 Q 100 130 95 130 L 75 130 Q 70 130 70 125 Z"
                    :fill="getHeatColor('Shoulders')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Shoulders')"
                    @mouseleave="hideTooltip"
                />
                <path 
                    id="shoulders-right-back"
                    d="M 300 95 Q 300 90 305 90 L 325 90 Q 330 90 330 95 L 330 125 Q 330 130 325 130 L 305 130 Q 300 130 300 125 Z"
                    :fill="getHeatColor('Shoulders')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Shoulders')"
                    @mouseleave="hideTooltip"
                />
                
                <!-- Back (center with slight taper) -->
                <path 
                    id="back"
                    d="M 175 80 L 225 80 L 220 260 L 180 260 Z"
                    :fill="getHeatColor('Back')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Back')"
                    @mouseleave="hideTooltip"
                />
                
                <!-- Lats (two shapes with curved outer edges) -->
                <path 
                    id="lats-left"
                    d="M 110 130 L 170 130 L 170 260 Q 110 265 110 150 Z"
                    :fill="getHeatColor('Lats')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Lats')"
                    @mouseleave="hideTooltip"
                />
                <path 
                    id="lats-right"
                    d="M 230 130 L 290 130 L 290 150 Q 290 265 230 260 Z"
                    :fill="getHeatColor('Lats')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Lats')"
                    @mouseleave="hideTooltip"
                />
                
                <!-- Triceps (elongated with slight curves) -->
                <path 
                    id="triceps-left"
                    d="M 70 140 Q 85 135 100 140 L 100 235 Q 85 240 70 235 Z"
                    :fill="getHeatColor('Triceps')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Triceps')"
                    @mouseleave="hideTooltip"
                />
                <path 
                    id="triceps-right"
                    d="M 300 140 Q 315 135 330 140 L 330 235 Q 315 240 300 235 Z"
                    :fill="getHeatColor('Triceps')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Triceps')"
                    @mouseleave="hideTooltip"
                />
                
                <!-- Glutes (wide with rounded bottom) -->
                <path 
                    id="glutes"
                    d="M 120 280 L 280 280 L 280 340 Q 200 350 120 340 Z"
                    :fill="getHeatColor('Glutes')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Glutes')"
                    @mouseleave="hideTooltip"
                />
                
                <!-- Hamstrings (two shapes with rounded edges) -->
                <path 
                    id="hamstrings-left"
                    d="M 125 375 Q 160 345 195 375 L 190 450 Q 160 480 130 450 Z"
                    :fill="getHeatColor('Hamstrings')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Hamstrings')"
                    @mouseleave="hideTooltip"
                />
                <path 
                    id="hamstrings-right"
                    d="M 205 375 Q 240 345 275 375 L 270 450 Q 240 480 210 450 Z"
                    :fill="getHeatColor('Hamstrings')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Hamstrings')"
                    @mouseleave="hideTooltip"
                />
                
                <!-- Calves (two shapes with curved tops and bottoms) -->
                <path 
                    id="calves-left"
                    d="M 140 490 Q 160 475 180 490 L 180 555 Q 160 570 140 555 Z"
                    :fill="getHeatColor('Calves')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Calves')"
                    @mouseleave="hideTooltip"
                />
                <path 
                    id="calves-right"
                    d="M 220 490 Q 240 475 260 490 L 260 555 Q 240 570 220 555 Z"
                    :fill="getHeatColor('Calves')"
                    fill-opacity="0.7"
                    class="muscle-group"
                    @mouseenter="showTooltip($event, 'Calves')"
                    @mouseleave="hideTooltip"
                />
            </g>
        </svg>
        
        <!-- View Toggle -->
        <div class="view-toggle">
            <v-btn 
                size="small" 
                :variant="view === 'front' ? 'flat' : 'outlined'"
                :color="view === 'front' ? 'primary' : ''"
                @click="view = 'front'"
            >
                Front
            </v-btn>
            <v-btn 
                size="small" 
                :variant="view === 'back' ? 'flat' : 'outlined'"
                :color="view === 'back' ? 'primary' : ''"
                @click="view = 'back'"
            >
                Back
            </v-btn>
        </div>
        
        <!-- Legend -->
        <div class="heatmap-legend">
            <div class="legend-title">Muscle Activation</div>
            <div class="legend-gradient">
                <div class="gradient-bar"></div>
                <div class="gradient-labels">
                    <span>Low</span>
                    <span>High</span>
                </div>
            </div>
        </div>
        
        <!-- Custom Tooltip -->
        <div 
            v-if="tooltipVisible" 
            class="custom-tooltip"
            :style="{ 
                left: tooltipX + 'px', 
                top: tooltipY + 'px' 
            }"
        >
            {{ tooltipContent }}
        </div>
    </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useWorkoutStore } from '@/stores/workout'
import { useExerciseStore } from '@/stores/exercise'

const workoutStore = useWorkoutStore()
const exerciseStore = useExerciseStore()

const { currentWorkout } = storeToRefs(workoutStore)
const { exercises: allExercises } = storeToRefs(exerciseStore)

const view = ref('front')

const tooltipVisible = ref(false)
const tooltipContent = ref('')
const tooltipX = ref(0)
const tooltipY = ref(0)

const emit = defineEmits(['muscle-clicked'])

const detailedWorkoutExercises = computed(() => {
  if (!currentWorkout.value.exercises) return []

  return currentWorkout.value.exercises.map(wExercise => {
    const fullExercise = allExercises.value.find(ex => 
      (wExercise.item_id && ex.item_id === wExercise.item_id) ||
      (ex.name === wExercise.name)
    )

    return {
      ...wExercise,
      exerciseDetails: fullExercise || wExercise.exerciseDetails || null
    }
  })
})

const muscleActivation = computed(() => {
  const activation = {}

  const allMuscles = [
    'Chest', 'Back', 'Shoulders', 'Biceps', 'Triceps',
    'Quadriceps', 'Hamstrings', 'Glutes', 'Calves',
    'Core', 'Forearms', 'Traps', 'Lats'
  ]

  allMuscles.forEach(muscle => {
    activation[muscle] = 0
  })

  detailedWorkoutExercises.value.forEach(exercise => {
    if (exercise.exerciseDetails) {
      const totalSets = exercise.sets?.length || 0
      exercise.exerciseDetails.muscles?.forEach(muscle => {
        activation[muscle] = (activation[muscle] || 0) + totalSets
      })
      exercise.exerciseDetails.sub_muscles?.forEach(muscle => {
        activation[muscle] = (activation[muscle] || 0) + totalSets * 0.5
      })
    }
  })

  return activation
})

const maxActivation = computed(() => {
  return Math.max(...Object.values(muscleActivation.value), 1)
})

function getHeatColor(muscle) {
  const activation = muscleActivation.value[muscle] || 0
  if (activation === 0) return '#f5f5f5'

  const intensity = activation / maxActivation.value

  if (intensity < 0.5) {
    const ratio = intensity * 2
    const r = 255
    const g = Math.round(255 - 127 * ratio)
    const b = 0
    return `rgb(${r}, ${g}, ${b})`
  } else {
    const ratio = (intensity - 0.5) * 2
    const r = 255
    const g = Math.round(128 - 128 * ratio)
    const b = 0
    return `rgb(${r}, ${g}, ${b})`
  }
}

function getMuscleTooltip(muscle) {
  const activation = muscleActivation.value[muscle] || 0
  const activationPercent = maxActivation.value > 0 ? Math.round((activation / maxActivation.value) * 100) : 0
  
  const exercises = detailedWorkoutExercises.value.filter(ex => {
    if (!ex.exerciseDetails) return false
    return (
      ex.exerciseDetails.muscles?.includes(muscle) || 
      ex.exerciseDetails.sub_muscles?.includes(muscle)
    )
  })
  
  let tooltip = `${muscle}: ${activationPercent}% activation`
  if (exercises.length > 0) {
    tooltip += `\nExercises: ${exercises.map(ex => ex.name).join(', ')}`
    tooltip += `\nTotal sets: ${activation}`
  }
  
  return tooltip
}

function showTooltip(event, muscle) {
  const rect = event.target.getBoundingClientRect()
  const containerRect = event.target.closest('.muscle-heatmap').getBoundingClientRect()
  
  tooltipContent.value = getMuscleTooltip(muscle)
  tooltipX.value = rect.left + rect.width / 2 - containerRect.left
  tooltipY.value = rect.top - containerRect.top - 10
  tooltipVisible.value = true
}

function hideTooltip() {
  tooltipVisible.value = false
}

function showMuscleInfo(muscle) {
  const activation = muscleActivation.value[muscle] || 0
  const activationPercent = (activation / maxActivation.value) * 100

  const exercises = detailedWorkoutExercises.value.filter(ex => {
    if (!ex.exerciseDetails) return false
    return (
      ex.exerciseDetails.muscles?.includes(muscle) || 
      ex.exerciseDetails.sub_muscles?.includes(muscle)
    )
  })

  emit('muscle-clicked', {
    muscle,
    activation: activationPercent / 100,
    exercises
  })
}

</script>

<style scoped>
.muscle-heatmap {
    position: relative;
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
}

.muscle-group {
    cursor: pointer;
    transition: all 0.3s ease;
}

.muscle-group:hover {
    stroke: #333;
    stroke-width: 2;
    filter: brightness(1.2);
    transform: scale(1.02);
    transform-origin: center;
}

.custom-tooltip {
    position: absolute;
    background: rgba(0, 0, 0, 0.9);
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 12px;
    white-space: pre-line;
    pointer-events: none;
    transform: translateX(-50%) translateY(-100%);
    z-index: 1000;
    max-width: 250px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.custom-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 5px solid transparent;
    border-top-color: rgba(0, 0, 0, 0.9);
}

.view-toggle {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 16px;
}

.heatmap-legend {
    margin-top: 24px;
    padding: 16px;
    background: rgba(0, 0, 0, 0.05);
    border-radius: 8px;
}

.legend-title {
    font-weight: 500;
    margin-bottom: 8px;
    text-align: center;
}

.gradient-bar {
    height: 20px;
    background: linear-gradient(to right, #ffff00, #ff8000, #ff0000);
    border-radius: 4px;
    margin-bottom: 4px;
}

.gradient-labels {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #666;
}
</style>