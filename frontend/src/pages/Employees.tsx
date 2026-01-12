import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, MoreHorizontal, MessageSquare, Phone, X } from 'lucide-react';
import api from '../lib/api';
import { cn } from '../lib/utils';

interface Employee {
    id: number;
    user: {
        email: string;
    };
    position: string;
    department_name: string;
    status: 'active' | 'on_leave' | 'terminated';
    profile_photo: string | null;
}

const COLUMNS = [
    { id: 'active', title: 'Active Staff', color: 'bg-green-500/10 text-green-700 border-green-200' },
    { id: 'on_leave', title: 'On Leave', color: 'bg-amber-500/10 text-amber-700 border-amber-200' },
    { id: 'terminated', title: 'Terminated', color: 'bg-red-500/10 text-red-700 border-red-200' },
];

export default function Employees() {
    const [employees, setEmployees] = useState<Employee[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [formData, setFormData] = useState({
        email: '',
        position: '',
        hire_date: new Date().toISOString().split('T')[0],
        status: 'active',
        contract_type: 'full_time'
    });

    useEffect(() => {
        fetchEmployees();
    }, []);

    const fetchEmployees = async () => {
        try {
            const response = await api.get('/employees/');
            setEmployees(response.data);
        } catch (error) {
            console.error("Failed to fetch employees", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreateEmployee = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.post('/employees/', formData);
            setShowModal(false);
            setFormData({
                email: '',
                position: '',
                hire_date: new Date().toISOString().split('T')[0],
                status: 'active',
                contract_type: 'full_time'
            });
            fetchEmployees(); // Refresh list
        } catch (error) {
            console.error("Failed to create employee", error);
            alert('Failed to create employee');
        }
    };

    const getColumnEmployees = (status: string) => employees.filter(e => e.status === status);

    if (isLoading) return <div className="p-8">Loading employees...</div>;

    return (
        <div className="h-full flex flex-col">
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Employees</h1>
                    <p className="text-slate-500 mt-1">Manage your team and their status</p>
                </div>
                <button
                    onClick={() => setShowModal(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl font-medium flex items-center gap-2 transition-colors shadow-lg shadow-blue-600/20"
                >
                    <Plus className="w-5 h-5" />
                    Add Employee
                </button>
            </div>

            {/* Add Employee Modal */}
            <AnimatePresence>
                {showModal && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
                        onClick={() => setShowModal(false)}
                    >
                        <motion.div
                            initial={{ scale: 0.95, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.95, opacity: 0 }}
                            onClick={e => e.stopPropagation()}
                            className="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl"
                        >
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-xl font-bold text-slate-800">Add New Employee</h2>
                                <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600">
                                    <X className="w-5 h-5" />
                                </button>
                            </div>

                            <form onSubmit={handleCreateEmployee} className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                                    <input
                                        type="email"
                                        required
                                        value={formData.email}
                                        onChange={e => setFormData({ ...formData, email: e.target.value })}
                                        className="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        placeholder="employee@company.com"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Position</label>
                                    <input
                                        type="text"
                                        required
                                        value={formData.position}
                                        onChange={e => setFormData({ ...formData, position: e.target.value })}
                                        className="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        placeholder="Software Engineer"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Hire Date</label>
                                    <input
                                        type="date"
                                        required
                                        value={formData.hire_date}
                                        onChange={e => setFormData({ ...formData, hire_date: e.target.value })}
                                        className="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Contract Type</label>
                                    <select
                                        value={formData.contract_type}
                                        onChange={e => setFormData({ ...formData, contract_type: e.target.value })}
                                        className="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    >
                                        <option value="full_time">Full Time</option>
                                        <option value="part_time">Part Time</option>
                                        <option value="contract">Contract</option>
                                        <option value="intern">Intern</option>
                                    </select>
                                </div>

                                <button
                                    type="submit"
                                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 rounded-lg transition-colors"
                                >
                                    Create Employee
                                </button>
                            </form>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            <div className="flex-1 overflow-x-auto">
                <div className="flex gap-6 h-full min-w-[1000px] pb-4">
                    {COLUMNS.map(column => (
                        <div key={column.id} className="flex-1 flex flex-col bg-slate-100/50 rounded-2xl p-4 border border-slate-200/60">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="font-semibold text-slate-700">{column.title}</h3>
                                <span className={cn("px-2.5 py-0.5 rounded-full text-xs font-semibold border", column.color)}>
                                    {getColumnEmployees(column.id).length}
                                </span>
                            </div>

                            <div className="flex-1 space-y-3 overflow-y-auto pr-2 custom-scrollbar">
                                <AnimatePresence>
                                    {getColumnEmployees(column.id).map(employee => (
                                        <motion.div
                                            key={employee.id}
                                            layoutId={String(employee.id)}
                                            initial={{ opacity: 0, y: 20 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            exit={{ opacity: 0, scale: 0.95 }}
                                            className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:shadow-md cursor-grab active:cursor-grabbing group transition-all"
                                        >
                                            <div className="flex items-start justify-between mb-3">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-10 h-10 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full flex items-center justify-center text-blue-700 font-bold border border-blue-200">
                                                        {employee.user.email[0].toUpperCase()}
                                                    </div>
                                                    <div>
                                                        <h4 className="font-semibold text-slate-800">{employee.user.email}</h4>
                                                        <p className="text-xs text-slate-500 font-medium">{employee.position}</p>
                                                    </div>
                                                </div>
                                                <button className="text-slate-300 hover:text-slate-600 opacity-0 group-hover:opacity-100 transition-opacity">
                                                    <MoreHorizontal className="w-5 h-5" />
                                                </button>
                                            </div>

                                            <div className="flex items-center gap-2 mt-4 pt-4 border-t border-slate-100">
                                                <div className="text-xs text-slate-400 font-medium px-2 py-1 bg-slate-50 rounded-md">
                                                    {employee.department_name || 'No Dept'}
                                                </div>
                                                <div className="flex-1" />
                                                <button className="p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                                                    <MessageSquare className="w-4 h-4" />
                                                </button>
                                                <button className="p-1.5 text-slate-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors">
                                                    <Phone className="w-4 h-4" />
                                                </button>
                                            </div>
                                        </motion.div>
                                    ))}
                                </AnimatePresence>

                                {getColumnEmployees(column.id).length === 0 && (
                                    <div className="h-32 flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-xl">
                                        <p className="text-sm font-medium">No employees found</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
