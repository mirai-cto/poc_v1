import api from './api'

// Generate tool recommendations
export const generateRecommendations = async (fileId, machineId) => {
  return api.post('/recommendations', { fileId, machineId })
}

// Get recommendations by ID
export const getRecommendations = async (recommendationId) => {
  return api.get(`/recommendations/${recommendationId}`)
}

// Update tool wear score
export const updateWearScore = async (recommendationId, toolId, wearScore) => {
  return api.patch(`/recommendations/${recommendationId}/wear-score`, {
    toolId,
    wearScore
  })
}

// Submit feedback for a recommendation
export const submitFeedback = async (recommendationId, feedback) => {
  return api.post(`/recommendations/${recommendationId}/feedback`, feedback)
}

// Mock implementation of generateRecommendations for development
export const mockGenerateRecommendations = async (fileId, machineId) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  // Return mock data
  return {
    id: 'rec-123',
    fileId,
    machineId,
    generatedAt: new Date().toISOString(),
    recommendations: [
      {
        operation: 'roughing',
        toolId: 102,
        toolName: 'End Mill 16mm 4-Flute',
        speedRpm: 8000,
        feedRate: 400,
        features: ['feature-004'],
        explanation: 'For roughing the pocket, a 16mm 4-flute end mill is selected as it efficiently removes material with its larger diameter. The 4 flutes provide good chip evacuation in aluminum. The pocket is 60x60mm, so a larger tool is more efficient for bulk material removal.'
      },
      {
        operation: 'finishing',
        toolId: 103,
        toolName: 'Ball End Mill 8mm',
        speedRpm: 10000,
        feedRate: 300,
        features: ['feature-004'],
        explanation: 'For finishing the pocket with 5mm corner radius, an 8mm ball end mill is recommended. This will produce a smooth surface finish and properly form the corner radius.'
      },
      {
        operation: 'finishing',
        toolId: 101,
        toolName: 'End Mill 10mm 2-Flute',
        speedRpm: 9500,
        feedRate: 350,
        features: ['feature-003'],
        explanation: 'For the 15mm wide slot, a 10mm end mill is optimal. The 2-flute design provides good chip evacuation in the confined slot space while machining aluminum.'
      },
      {
        operation: 'drilling',
        toolId: 105,
        toolName: 'Drill 12mm',
        speedRpm: 7000,
        feedRate: 220,
        features: ['feature-001'],
        explanation: 'For the 12.5mm diameter hole, a 12mm drill is selected for the initial hole. This can be followed by a boring operation for the precise diameter if required.'
      },
      {
        operation: 'drilling',
        toolId: 104,
        toolName: 'Drill 8.5mm',
        speedRpm: 6000,
        feedRate: 180,
        features: ['feature-002'],
        explanation: 'For the 8mm diameter hole, an 8.5mm drill is recommended. This slightly larger drill allows for finishing to the exact dimension if needed.'
      }
    ],
    summary: 'The tool selection is optimized for machining aluminum 6061 on a Haas VF-2 machine. For the pocket, a roughing operation with a 16mm end mill followed by finishing with an 8mm ball end mill is recommended. The slot can be machined with a 10mm end mill. For holes, 12mm and 8.5mm drills are selected. All speeds and feeds are set for optimal aluminum machining while staying within the machine\'s capabilities.'
  }
}

// Mock implementation of updateWearScore for development
export const mockUpdateWearScore = async (recommendationId, toolId, wearScore) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500))
  
  // Return success response
  return {
    success: true,
    recommendationId,
    toolId,
    wearScore,
    adjustedSpeedRpm: Math.floor(10000 / wearScore * 8),
    adjustedFeedRate: Math.floor(400 / wearScore * 9)
  }
}

// Mock implementation of submitFeedback for development
export const mockSubmitFeedback = async (recommendationId, feedback) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 800))
  
  // Return success response
  return {
    success: true,
    recommendationId,
    feedbackId: 'feedback-' + Math.floor(Math.random() * 1000),
    submittedAt: new Date().toISOString()
  }
} 