import { Routes, Route } from 'react-router-dom'
import { lazy, Suspense } from 'react'

// Layouts
import Layout from './components/Layout/Layout'

// Pages
const Home = lazy(() => import('./pages/Home/Home'))
const FileUpload = lazy(() => import('./pages/FileUpload/FileUpload'))
const FeatureViewer = lazy(() => import('./pages/FeatureViewer/FeatureViewer'))
const MachineSelection = lazy(() => import('./pages/MachineSelection/MachineSelection'))
const Recommendations = lazy(() => import('./pages/Recommendations/Recommendations'))
const Feedback = lazy(() => import('./pages/Feedback/Feedback'))
const NotFound = lazy(() => import('./pages/NotFound/NotFound'))

// Loading component
const LoadingComponent = () => (
  <div className="container" style={{ textAlign: 'center', padding: '5rem 0' }}>
    <h2>Loading...</h2>
  </div>
)

function App() {
  return (
    <Suspense fallback={<LoadingComponent />}>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="upload" element={<FileUpload />} />
          <Route path="features/:fileId" element={<FeatureViewer />} />
          <Route path="select-machine/:fileId" element={<MachineSelection />} />
          <Route path="recommendations/:fileId" element={<Recommendations />} />
          <Route path="feedback/:recommendationId" element={<Feedback />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </Suspense>
  )
}

export default App 