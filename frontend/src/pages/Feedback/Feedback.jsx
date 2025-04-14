import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const Feedback = () => {
  const { recommendationId } = useParams();
  const navigate = useNavigate();
  
  const [rating, setRating] = useState(null);
  const [comments, setComments] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleRatingChange = (value) => {
    setRating(value);
  };

  const handleCommentsChange = (e) => {
    setComments(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!rating) {
      alert('Please select a rating');
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      // In a real app, this would submit to the API
      console.log('Submitting feedback:', {
        recommendationId,
        rating,
        comments
      });
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSubmitted(true);
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBackToHome = () => {
    navigate('/');
  };

  if (submitted) {
    return (
      <div className="container">
        <div className="alert alert-success" role="alert">
          <h4 className="alert-heading">Thank you for your feedback!</h4>
          <p>Your feedback has been submitted successfully. This helps us improve our recommendations.</p>
          <hr />
          <button className="btn btn-primary" onClick={handleBackToHome}>
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Provide Feedback</h1>
      <p>For recommendation ID: {recommendationId}</p>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="form-label">How satisfied are you with this recommendation?</label>
          <div className="rating-buttons">
            {[1, 2, 3, 4, 5].map(value => (
              <button
                key={value}
                type="button"
                className={`btn ${rating === value ? 'btn-primary' : 'btn-outline-primary'} me-2`}
                onClick={() => handleRatingChange(value)}
              >
                {value}
              </button>
            ))}
          </div>
          <div className="mt-2 text-muted">
            <small>1 = Not satisfied, 5 = Very satisfied</small>
          </div>
        </div>
        
        <div className="mb-4">
          <label htmlFor="comments" className="form-label">Comments (optional)</label>
          <textarea
            id="comments"
            className="form-control"
            rows="3"
            value={comments}
            onChange={handleCommentsChange}
            placeholder="Share your experience with this tool recommendation..."
          ></textarea>
        </div>
        
        <div className="d-flex">
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
          </button>
          <button
            type="button"
            className="btn btn-outline-secondary ms-2"
            onClick={() => navigate(-1)}
          >
            Back
          </button>
        </div>
      </form>
    </div>
  );
};

export default Feedback; 