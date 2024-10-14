import { Route, Routes } from "react-router-dom"; 
import Home from "./Home";
import Navbar from "./Navbar";
import Restaurant from "./Restaurant";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/restaurants" element={<Home />} />
        <Route path="/restaurants/:id" element={<Restaurant />} /> 
        <Route path="/" element={<Home />} />
      </Routes>
    </>
  );
}

export default App;
