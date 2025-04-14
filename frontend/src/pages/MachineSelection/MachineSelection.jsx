import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const MachineSelection = () => {
  const { fileId } = useParams();
  const navigate = useNavigate();
  const [machines, setMachines] = useState([]);
  const [selectedMachine, setSelectedMachine] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMachines = async () => {
      try {
        // In a real app, this would fetch from the API
        setMachines([
          { id: 1, name: 'Haas VF-2', model: 'VF-2', manufacturer: 'Haas', maxRpm: 12000 },
          { id: 2, name: 'DMG MORI DMU 50', model: 'DMU 50', manufacturer: 'DMG MORI', maxRpm: 18000 },
          { id: 3, name: 'Tormach PCNC 1100', model: 'PCNC 1100', manufacturer: 'Tormach', maxRpm: 5000 }
        ]);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching machines:', error);
        setLoading(false);
      }
    };

    fetchMachines();
  }, []);

  const handleMachineSelect = (machineId) => {
    setSelectedMachine(machineId);
  };

  const handleContinue = () => {
    if (selectedMachine) {
      navigate(`/recommendations/${fileId}?machineId=${selectedMachine}`);
    } else {
      alert('Please select a machine to continue');
    }
  };

  if (loading) {
    return <div className="container"><h2>Loading machines...</h2></div>;
  }

  return (
    <div className="container">
      <h1>Machine Selection</h1>
      <p>Select a machine for processing file ID: {fileId}</p>

      <div className="machines-list">
        {machines.length === 0 ? (
          <p>No machines available. Please add machines to the system.</p>
        ) : (
          <div className="row">
            {machines.map(machine => (
              <div className="col-md-4 mb-4" key={machine.id}>
                <div 
                  className={`card ${selectedMachine === machine.id ? 'border-primary' : ''}`}
                  onClick={() => handleMachineSelect(machine.id)}
                  style={{ cursor: 'pointer' }}
                >
                  <div className="card-body">
                    <h5 className="card-title">{machine.name}</h5>
                    <p className="card-text">
                      <strong>Model:</strong> {machine.model}<br />
                      <strong>Manufacturer:</strong> {machine.manufacturer}<br />
                      <strong>Max RPM:</strong> {machine.maxRpm.toLocaleString()}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      <button 
        className="btn btn-primary mt-4" 
        onClick={handleContinue}
        disabled={!selectedMachine}
      >
        Continue to Recommendations
      </button>
    </div>
  );
};

export default MachineSelection; 