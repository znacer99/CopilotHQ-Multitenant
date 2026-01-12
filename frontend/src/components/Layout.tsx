import { useState, useEffect } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import {
    LayoutDashboard,
    Users,
    Briefcase,
    FileText,
    CreditCard,
    Settings,
    LogOut,
    Menu,
    X,
    Bot,
    Bell
} from 'lucide-react';
import { cn } from '../lib/utils';
import { motion } from 'framer-motion';
import api from '../lib/api';

const SidebarItem = ({ icon: Icon, label, path, isActive }: { icon: any, label: string, path: string, isActive: boolean }) => (
    <Link
        to={path}
        className={cn(
            "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group",
            isActive
                ? "bg-blue-600 text-white shadow-lg shadow-blue-600/20"
                : "text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800"
        )}
    >
        <Icon className={cn("w-5 h-5", isActive ? "text-white" : "text-slate-500 group-hover:text-blue-600")} />
        <span className="font-medium">{label}</span>
    </Link>
);

export default function Layout() {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const [tenantName, setTenantName] = useState('Loading...');
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        api.get('/tenant/')
            .then(res => setTenantName(res.data.name))
            .catch(() => setTenantName('Unknown'));
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', path: '/dashboard' },
        { icon: Users, label: 'Employees', path: '/employees' },
        { icon: Briefcase, label: 'Recruiting', path: '/recruiting' },
        { icon: FileText, label: 'Documents', path: '/documents' },
        { icon: CreditCard, label: 'Payroll', path: '/payroll' },
        { icon: Settings, label: 'Settings', path: '/settings' },
    ];

    return (
        <div className="min-h-screen bg-slate-50 flex">
            {/* Sidebar */}
            <motion.aside
                initial={{ width: 280 }}
                animate={{ width: isSidebarOpen ? 280 : 80 }}
                className="bg-white border-r border-slate-200 h-screen sticky top-0 flex flex-col z-20"
            >
                <div className="p-6 flex items-center justify-between">
                    <div className={cn("flex items-center gap-2 overflow-hidden", !isSidebarOpen && "justify-center")}>
                        <div className="w-8 h-8 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center shrink-0">
                            <Bot className="w-5 h-5 text-white" />
                        </div>
                        {isSidebarOpen && <span className="font-bold text-xl text-slate-800">CopilotHQ</span>}
                    </div>
                    <button
                        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                        className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors lg:block hidden"
                    >
                        {isSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                    </button>
                </div>

                <nav className="flex-1 px-4 py-4 space-y-2 overflow-y-auto">
                    {navItems.map((item) => (
                        <SidebarItem
                            key={item.path}
                            {...item}
                            isActive={location.pathname === item.path}
                        />
                    ))}
                </nav>

                <div className="p-4 border-t border-slate-100">
                    <button
                        onClick={handleLogout}
                        className={cn(
                            "flex items-center gap-3 w-full px-4 py-3 text-red-500 hover:bg-red-50 rounded-xl transition-colors",
                            !isSidebarOpen && "justify-center"
                        )}
                    >
                        <LogOut className="w-5 h-5" />
                        {isSidebarOpen && <span className="font-medium">Sign Out</span>}
                    </button>
                </div>
            </motion.aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
                {/* Topbar */}
                <header className="h-16 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10">
                    <div className="text-sm text-slate-500">
                        Organization: <span className="font-semibold text-slate-800">{tenantName}</span>
                    </div>

                    <div className="flex items-center gap-6">
                        <button className="relative p-2 text-slate-400 hover:bg-slate-100 rounded-full transition-colors">
                            <Bell className="w-5 h-5" />
                            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
                        </button>
                        <div className="flex items-center gap-3">
                            <div className="w-9 h-9 bg-slate-200 rounded-full flex items-center justify-center text-slate-600 font-semibold border border-slate-300">
                                JD
                            </div>
                            <div className="hidden md:block text-sm">
                                <p className="font-medium text-slate-800">John Doe</p>
                                <p className="text-slate-500 text-xs">HR Manager</p>
                            </div>
                        </div>
                    </div>
                </header>

                {/* Page Content */}
                <div className="flex-1 overflow-auto p-8 relative">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}
