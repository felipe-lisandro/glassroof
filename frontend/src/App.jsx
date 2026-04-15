import { AppRoutes } from './routes'
import Navbar from './components/Navbar'
import Footer from './components/Footer'

function App() {
  return (
    <>
      <Navbar/>
      <AppRoutes />
      <Footer/>
    </>
  )
}

export default App