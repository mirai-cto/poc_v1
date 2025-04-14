import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from 'react-query'
import { toast } from 'react-toastify'
import styled from 'styled-components'
import { useDropzone } from 'react-dropzone'

// API service import would go here
// import { uploadCADFile } from '../../services/cadService'

const PageTitle = styled.h1`
  margin-bottom: 2rem;
  color: var(--secondary-color);
`

const UploadContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
`

const DropzoneContainer = styled.div`
  border: 2px dashed var(--primary-color);
  border-radius: 0.5rem;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  background-color: ${props => props.isDragActive ? 'rgba(37, 99, 235, 0.1)' : 'white'};
  transition: background-color 0.2s;
  margin-bottom: 2rem;
`

const UploadIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
`

const UploadText = styled.p`
  margin-bottom: 1rem;
  color: var(--text-color);
  font-size: 1.125rem;
`

const SupportedFormats = styled.p`
  color: var(--dark-gray);
  font-size: 0.875rem;
`

const UploadButton = styled.button`
  padding: 0.75rem 2rem;
  font-size: 1.125rem;
  font-weight: 600;
  margin-top: 1rem;
  width: 100%;
`

const FileInfo = styled.div`
  margin-top: 2rem;
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`

const FileInfoItem = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
`

const FileInfoLabel = styled.span`
  font-weight: 500;
  width: 120px;
`

const FileInfoValue = styled.span`
  color: var(--dark-gray);
`

const FileUpload = () => {
  const navigate = useNavigate()
  const [selectedFile, setSelectedFile] = useState(null)
  
  // Mock upload mutation
  // In a real implementation, this would use a real API call
  const uploadMutation = useMutation((formData) => {
    // Simulate API call
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ id: 'mockFileId123' })
      }, 1500)
    })
  }, {
    onSuccess: (data) => {
      toast.success('File uploaded successfully!')
      // Navigate to features page
      navigate(`/features/${data.id}`)
    },
    onError: (error) => {
      toast.error('Failed to upload file: ' + error.message)
    }
  })
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/step': ['.stp', '.step'],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setSelectedFile(acceptedFiles[0])
      }
    }
  })
  
  const handleUpload = () => {
    if (!selectedFile) {
      toast.warning('Please select a file first')
      return
    }
    
    const formData = new FormData()
    formData.append('file', selectedFile)
    
    uploadMutation.mutate(formData)
  }
  
  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' bytes'
    else if (bytes < 1048576) return (bytes / 1024).toFixed(2) + ' KB'
    else return (bytes / 1048576).toFixed(2) + ' MB'
  }
  
  return (
    <UploadContainer>
      <PageTitle>Upload CAD File</PageTitle>
      
      <DropzoneContainer {...getRootProps()} isDragActive={isDragActive}>
        <input {...getInputProps()} />
        <UploadIcon>📁</UploadIcon>
        <UploadText>
          {isDragActive
            ? 'Drop the file here'
            : 'Drag and drop your CAD file here, or click to select'}
        </UploadText>
        <SupportedFormats>Supported formats: .stp, .step</SupportedFormats>
      </DropzoneContainer>
      
      {selectedFile && (
        <FileInfo>
          <h3 style={{ marginBottom: '1rem' }}>Selected File</h3>
          <FileInfoItem>
            <FileInfoLabel>Name:</FileInfoLabel>
            <FileInfoValue>{selectedFile.name}</FileInfoValue>
          </FileInfoItem>
          <FileInfoItem>
            <FileInfoLabel>Size:</FileInfoLabel>
            <FileInfoValue>{formatFileSize(selectedFile.size)}</FileInfoValue>
          </FileInfoItem>
          <FileInfoItem>
            <FileInfoLabel>Type:</FileInfoLabel>
            <FileInfoValue>{selectedFile.type || 'application/step'}</FileInfoValue>
          </FileInfoItem>
        </FileInfo>
      )}
      
      <UploadButton 
        className="btn" 
        onClick={handleUpload}
        disabled={!selectedFile || uploadMutation.isLoading}
      >
        {uploadMutation.isLoading ? 'Uploading...' : 'Upload'}
      </UploadButton>
    </UploadContainer>
  )
}

export default FileUpload 