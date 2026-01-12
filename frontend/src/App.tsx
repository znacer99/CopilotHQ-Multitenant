import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Employees from './pages/Employees';
import Recruiting from './pages/Recruiting';
import Leave from './pages/Leave';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        {/* Protected Routes */}
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/employees" element={<Employees />} />
          <Route path="/recruiting" element={<Recruiting />} />
          <Route path="/documents" element={<div className="p-8 text-slate-500">Documents Module (Coming Soon)</div>} />
          <Route path="/payroll" element={<div className="p-8 text-slate-500">Payroll Module (Coming Soon)</div>} />
          <Route path="/leave" element={<Leave />} />
          <Route path="/settings" element={<div className="p-8 text-slate-500">Settings (Coming Soon)</div>} />
        </Route>

        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
