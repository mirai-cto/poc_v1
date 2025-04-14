import { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';

const Recommendations = () => {
  const { fileId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const machineId = queryParams.get('machineId');
  
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        // In a real app, this would fetch from the API
        setRecommendations([
          { 
            id: 1, 
            toolName: 'End Mill 10mm 4-Flute', 
            operation: 'roughing',
            recommendedSpeed: 12000,
            recommendedFeed: 1200,
            wearScore: null 
          },
          { 
            id: 2, 
            toolName: 'Ball End Mill 6mm 2-Flute', 
            operation: 'finishing',
            recommendedSpeed: 15000,
            recommendedFeed: 900,
            wearScore: null 
          },
          { 
            id: 3, 
            toolName: 'Drill Bit 8mm HSS', 
            operation: 'drilling',
            recommendedSpeed: 10000,
            recommendedFeed: 800,
            wearScore: null 
          }
        ]);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
        setLoading(false);
      }
    };

    if (fileId && machineId) {
      fetchRecommendations();
    } else {
      setLoading(false);
    }
  }, [fileId, machineId]);

  const handleWearScoreChange = (id, value) => {
    setRecommendations(prevRecs => 
      prevRecs.map(rec => 
        rec.id === id ? { ...rec, wearScore: parseInt(value) } : rec
      )
    );
  };

  const handleSubmitFeedback = (recommendationId) => {
    navigate(`/feedback/${recommendationId}`);
  };

  if (loading) {
    return <div className="container"><h2>Loading recommendations...</h2></div>;
  }

  if (!machineId) {
    return (
      <div className="container">
        <h1>Error</h1>
        <p>No machine selected. Please go back and select a machine.</p>
        <button 
          className="btn btn-primary" 
          onClick={() => navigate(`/select-machine/${fileId}`)}
        >
          Back to Machine Selection
        </button>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Tool Recommendations</h1>
      <p>Recommendations for file ID: {fileId} with machine ID: {machineId}</p>

      {recommendations.length === 0 ? (
        <p>No recommendations found.</p>
      ) : (
        <div className="recommendations-list">
          <table className="table">
            <thead>
              <tr>
                <th>Tool</th>
                <th>Operation</th>
                <th>Recommended Speed (RPM)</th>
                <th>Recommended Feed (mm/min)</th>
                <th>Tool Wear Score (1-10)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {recommendations.map(rec => (
                <tr key={rec.id}>
                  <td>{rec.toolName}</td>
                  <td>
                    <span className="text-capitalize">{rec.operation}</span>
                  </td>
                  <td>{rec.recommendedSpeed.toLocaleString()}</td>
                  <td>{rec.recommendedFeed.toLocaleString()}</td>
                  <td>
                    <select 
                      className="form-select"
                      value={rec.wearScore || ''}
                      onChange={(e) => handleWearScoreChange(rec.id, e.target.value)}
                    >
                      <option value="">Select score</option>
                      {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
                        <option key={num} value={num}>{num}</option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <button 
                      className="btn btn-sm btn-outline-primary"
                      onClick={() => handleSubmitFeedback(rec.id)}
                    >
                      Submit Feedback
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Recommendations; 