import { BrowserRouter } from "react-router-dom"

import AppRoutes from "./routes"
import Navbar from "./components/Navbar"    
import Footer from "./components/Footer"

function App() {
  return (
    <BrowserRouter basename={import.meta.env.BASE_URL}>
      <Navbar />
      <AppRoutes />
      <Footer />
    </BrowserRouter>
  )
}

export default App