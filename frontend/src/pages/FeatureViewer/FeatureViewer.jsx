import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const FeatureViewer = () => {
  const { fileId } = useParams();
  const navigate = useNavigate();
  const [features, setFeatures] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFeatures = async () => {
      try {
        // In a real app, this would fetch from the API
        setFeatures([
          { id: 1, type: 'hole', x: 10, y: 20, depth: 5, diameter: 8 },
          { id: 2, type: 'pocket', x: 50, y: 60, depth: 10, width: 30, height: 20 }
        ]);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching features:', error);
        setLoading(false);
      }
    };

    fetchFeatures();
  }, [fileId]);

  const handleContinue = () => {
    navigate(`/select-machine/${fileId}`);
  };

  if (loading) {
    return <div className="container"><h2>Loading features...</h2></div>;
  }

  return (
    <div className="container">
      <h1>Feature Viewer</h1>
      <p>Viewing features for file ID: {fileId}</p>
      
      <div className="feature-list">
        <h2>Extracted Features</h2>
        {features.length === 0 ? (
          <p>No features found in this file.</p>
        ) : (
          <ul>
            {features.map(feature => (
              <li key={feature.id}>
                <strong>{feature.type}</strong>: 
                Position: ({feature.x}, {feature.y}), 
                {feature.diameter && ` Diameter: ${feature.diameter}mm,`}
                {feature.width && ` Width: ${feature.width}mm,`}
                {feature.height && ` Height: ${feature.height}mm,`}
                {feature.depth && ` Depth: ${feature.depth}mm`}
              </li>
            ))}
          </ul>
        )}
      </div>
      
      <button 
        className="btn btn-primary" 
        onClick={handleContinue}
      >
        Continue to Machine Selection
      </button>
    </div>
  );
};

export default FeatureViewer; 