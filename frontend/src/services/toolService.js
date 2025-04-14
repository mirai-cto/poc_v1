import api from './api'

// Get all tools
export const getTools = async () => {
  return api.get('/tools')
}

// Get a tool by ID
export const getTool = async (toolId) => {
  return api.get(`/tools/${toolId}`)
}

// Filter tools by constraints
export const filterTools = async (filters) => {
  return api.get('/tools/filter', { params: filters })
}

// Mock implementation of getTools for development
export const mockGetTools = async () => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 800))
  
  // Return mock data
  return [
    {
      id: 101,
      name: 'End Mill 10mm 2-Flute',
      type: 'end_mill',
      material: 'carbide',
      diameter: 10.0,
      flute_count: 2,
      overall_length: 75.0,
      cutting_length: 25.0,
      shank_diameter: 10.0,
      max_doc: 15.0,
      max_rpm: 18000,
      manufacturer: 'Sandvik'
    },
    {
      id: 102,
      name: 'End Mill 16mm 4-Flute',
      type: 'end_mill',
      material: 'carbide',
      diameter: 16.0,
      flute_count: 4,
      overall_length: 100.0,
      cutting_length: 32.0,
      shank_diameter: 16.0,
      max_doc: 24.0,
      max_rpm: 12000,
      manufacturer: 'Kennametal'
    },
    {
      id: 103,
      name: 'Ball End Mill 8mm',
      type: 'ball_end_mill',
      material: 'carbide',
      diameter: 8.0,
      flute_count: 2,
      overall_length: 60.0,
      cutting_length: 20.0,
      shank_diameter: 8.0,
      max_doc: 12.0,
      max_rpm: 20000,
      manufacturer: 'Iscar'
    },
    {
      id: 104,
      name: 'Drill 8.5mm',
      type: 'drill',
      material: 'hss',
      diameter: 8.5,
      overall_length: 80.0,
      cutting_length: 45.0,
      shank_diameter: 8.5,
      max_doc: 42.0,
      max_rpm: 10000,
      manufacturer: 'Guhring'
    },
    {
      id: 105,
      name: 'Drill 12mm',
      type: 'drill',
      material: 'carbide',
      diameter: 12.0,
      overall_length: 95.0,
      cutting_length: 55.0,
      shank_diameter: 12.0,
      max_doc: 50.0,
      max_rpm: 12000,
      manufacturer: 'Walter'
    }
  ]
}

// Mock implementation of getTool for development
export const mockGetTool = async (toolId) => {
  const tools = await mockGetTools()
  const tool = tools.find(t => t.id === Number(toolId))
  
  if (!tool) {
    throw new Error('Tool not found')
  }
  
  return tool
}

// Mock implementation of filterTools for development
export const mockFilterTools = async (filters) => {
  const tools = await mockGetTools()
  
  return tools.filter(tool => {
    // Filter by type
    if (filters.type && tool.type !== filters.type) {
      return false
    }
    
    // Filter by material
    if (filters.material && tool.material !== filters.material) {
      return false
    }
    
    // Filter by diameter range
    if (filters.minDiameter && tool.diameter < filters.minDiameter) {
      return false
    }
    if (filters.maxDiameter && tool.diameter > filters.maxDiameter) {
      return false
    }
    
    // Filter by manufacturer
    if (filters.manufacturer && !tool.manufacturer.toLowerCase().includes(filters.manufacturer.toLowerCase())) {
      return false
    }
    
    return true
  })
} 