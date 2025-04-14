import api from './api'

// Upload a CAD file
export const uploadCADFile = async (fileData) => {
  const formData = new FormData()
  formData.append('file', fileData)
  
  // For file uploads, we need to override the Content-Type header
  return api.post('/cad-files', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

// Get a CAD file by ID
export const getCADFile = async (fileId) => {
  return api.get(`/cad-files/${fileId}`)
}

// Get features for a CAD file
export const getCADFeatures = async (fileId) => {
  return api.get(`/cad-files/${fileId}/features`)
}

// Mock implementation of getCADFeatures for development
export const mockGetCADFeatures = async (fileId) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // Return mock data
  return {
    id: fileId,
    filename: 'engine_block.step',
    features: [
      {
        id: 'feature-001',
        name: 'Hole_1',
        type: 'hole',
        confidence: 0.98,
        x: 10.0,
        y: 20.0,
        z: 0.0,
        diameter: 12.5,
        depth: 25.0
      },
      {
        id: 'feature-002',
        name: 'Hole_2',
        type: 'hole',
        confidence: 0.95,
        x: 50.0,
        y: 20.0,
        z: 0.0,
        diameter: 8.0,
        depth: 15.0
      },
      {
        id: 'feature-003',
        name: 'Slot_1',
        type: 'slot',
        confidence: 0.92,
        x: 100.0,
        y: 50.0,
        z: 0.0,
        width: 15.0,
        length: 80.0,
        depth: 10.0
      },
      {
        id: 'feature-004',
        name: 'Pocket_1',
        type: 'pocket',
        confidence: 0.88,
        x: 150.0,
        y: 100.0,
        z: 0.0,
        width: 60.0,
        length: 60.0,
        depth: 30.0,
        corner_radius: 5.0
      }
    ],
    metadata: {
      units: 'mm',
      source_file: 'engine_block.step',
      parsed_at: '2023-07-15T12:00:00Z',
      material: 'aluminum 6061',
      part_name: 'Engine Block Prototype'
    }
  }
} 