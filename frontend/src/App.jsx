import { BrowserRouter } from "react-router-dom"

import { AuthProvider } from "./contexts/AuthContext"
import AppRoutes from "./routes"
import Navbar from "./components/Navbar"
import Footer from "./components/Footer"

function App() {
  return (
    <BrowserRouter basename={import.meta.env.BASE_URL}>
      <AuthProvider>
        <Navbar />
        <AppRoutes />
        <Footer />
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
