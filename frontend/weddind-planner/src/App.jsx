import { BrowserRouter, Routes, Route } from "react-router-dom";
import WeddingDashboard from "./pages/wedding-dashboard";
import Layout from "./pages/layout";
import TestDrawer from "./pages/TestDrawer";
import LoginPage from "./pages/Login";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<WeddingDashboard />} />
          <Route path="/test" element={<TestDrawer />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
