import api from './api'

// Get all machines
export const getMachines = async () => {
  return api.get('/machines')
}

// Get a machine by ID
export const getMachine = async (machineId) => {
  return api.get(`/machines/${machineId}`)
}

// Mock implementation of getMachines for development
export const mockGetMachines = async () => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 800))
  
  // Return mock data
  return [
    {
      id: 1,
      name: 'Haas VF-2',
      model: 'VF-2',
      manufacturer: 'Haas',
      max_rpm: 12000,
      max_feed_rate: 500.0,
      spindle_power: 22.4,
      max_tool_diameter: 89.0,
      min_tool_diameter: 0.5
    },
    {
      id: 2,
      name: 'DMG Mori NLX 2500',
      model: 'NLX 2500',
      manufacturer: 'DMG Mori',
      max_rpm: 4000,
      max_feed_rate: 300.0,
      spindle_power: 18.5,
      max_tool_diameter: 76.0,
      min_tool_diameter: 1.0
    },
    {
      id: 3,
      name: 'Mazak INTEGREX i-200S',
      model: 'INTEGREX i-200S',
      manufacturer: 'Mazak',
      max_rpm: 12000,
      max_feed_rate: 450.0,
      spindle_power: 30.0,
      max_tool_diameter: 90.0,
      min_tool_diameter: 0.8
    },
    {
      id: 4,
      name: 'Okuma GENOS M560-V',
      model: 'GENOS M560-V',
      manufacturer: 'Okuma',
      max_rpm: 15000,
      max_feed_rate: 550.0,
      spindle_power: 22.0,
      max_tool_diameter: 80.0,
      min_tool_diameter: 0.5
    }
  ]
}

// Mock implementation of getMachine for development
export const mockGetMachine = async (machineId) => {
  const machines = await mockGetMachines()
  const machine = machines.find(m => m.id === Number(machineId))
  
  if (!machine) {
    throw new Error('Machine not found')
  }
  
  return machine
} 