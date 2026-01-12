import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, X, User, Mail, Sparkles } from 'lucide-react';
import api from '../lib/api';
import { cn } from '../lib/utils';

interface Candidate {
    id: number;
    name: string;
    email: string;
    phone: string | null;
    position: string | null;
    status: 'applied' | 'screening' | 'interview' | 'offer' | 'hired' | 'rejected';
    ai_score: number;
    created_at: string;
}

const COLUMNS = [
    { id: 'applied', title: 'Applied', color: 'bg-slate-500/10 text-slate-700 border-slate-300' },
    { id: 'screening', title: 'Screening', color: 'bg-blue-500/10 text-blue-700 border-blue-200' },
    { id: 'interview', title: 'Interview', color: 'bg-purple-500/10 text-purple-700 border-purple-200' },
    { id: 'offer', title: 'Offer', color: 'bg-amber-500/10 text-amber-700 border-amber-200' },
    { id: 'hired', title: 'Hired', color: 'bg-green-500/10 text-green-700 border-green-200' },
];

export default function Recruiting() {
    const [candidates, setCandidates] = useState<Candidate[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        position: '',
        status: 'applied'
    });

    useEffect(() => {
        fetchCandidates();
    }, []);

    const fetchCandidates = async () => {
        try {
            const response = await api.get('/candidates/');
            setCandidates(response.data);
        } catch (error) {
            console.error("Failed to fetch candidates", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreateCandidate = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.post('/candidates/', formData);
            setShowModal(false);
            setFormData({ name: '', email: '', phone: '', position: '', status: 'applied' });
            fetchCandidates();
        } catch (error) {
            console.error("Failed to create candidate", error);
            alert('Failed to create candidate');
        }
    };

    const handleStatusChange = async (candidateId: number, newStatus: string) => {
        try {
            await api.patch(`/candidates/${candidateId}/`, { status: newStatus });
            fetchCandidates();
        } catch (error) {
            console.error("Failed to update status", error);
        }
    };

    const getColumnCandidates = (status: string) => candidates.filter(c => c.status === status);

    if (isLoading) return <div className="p-8">Loading candidates...</div>;

    return (
        <div className="h-full flex flex-col">
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Recruiting Pipeline</h1>
                    <p className="text-slate-500 mt-1">Track candidates through your hiring process</p>
                </div>
                <button
                    onClick={() => setShowModal(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl font-medium flex items-center gap-2 transition-colors shadow-lg shadow-blue-600/20"
                >
                    <Plus className="w-5 h-5" />
                    Add Candidate
                </button>
            </div>

            {/* Add Candidate Modal */}
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
                                <h2 className="text-xl font-bold text-slate-800">Add New Candidate</h2>
                                <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600">
                                    <X className="w-5 h-5" />
                                </button>
                            </div>

                            <form onSubmit={handleCreateCandidate} className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
                                    <input
                                        type="text"
                                        required
                                        value={formData.name}
                                        onChange={e => setFormData({ ...formData, name: e.target.value })}
                                        className="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        placeholder="John Doe"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                                    <input
                                        type="email"
                                        required
                                        value={formData.email}
                                        onChange={e => setFormData({ ...formData, email: e.target.value })}
                                        className="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        placeholder="john@example.com"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Phone</label>
                                    <input
                                        type="text"
                                        value={formData.phone}
                                        onChange={e => setFormData({ ...formData, phone: e.target.value })}
                                        className="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        placeholder="+1 234 567 890"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Position Applied</label>
                                    <input
                                        type="text"
                                        value={formData.position}
                                        onChange={e => setFormData({ ...formData, position: e.target.value })}
                                        className="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        placeholder="Software Engineer"
                                    />
                                </div>

                                <button
                                    type="submit"
                                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 rounded-lg transition-colors"
                                >
                                    Add Candidate
                                </button>
                            </form>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Kanban Board */}
            <div className="flex-1 overflow-x-auto">
                <div className="flex gap-4 h-full min-w-[1200px] pb-4">
                    {COLUMNS.map(column => (
                        <div key={column.id} className="flex-1 flex flex-col bg-slate-100/50 rounded-2xl p-4 border border-slate-200/60 min-w-[220px]">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="font-semibold text-slate-700">{column.title}</h3>
                                <span className={cn("px-2.5 py-0.5 rounded-full text-xs font-semibold border", column.color)}>
                                    {getColumnCandidates(column.id).length}
                                </span>
                            </div>

                            <div className="flex-1 space-y-3 overflow-y-auto pr-2">
                                <AnimatePresence>
                                    {getColumnCandidates(column.id).map(candidate => (
                                        <motion.div
                                            key={candidate.id}
                                            layoutId={String(candidate.id)}
                                            initial={{ opacity: 0, y: 20 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            exit={{ opacity: 0, scale: 0.95 }}
                                            className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:shadow-md group transition-all"
                                        >
                                            <div className="flex items-start justify-between mb-2">
                                                <div className="flex items-center gap-2">
                                                    <div className="w-8 h-8 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center text-purple-700 font-bold text-sm border border-purple-200">
                                                        {candidate.name[0].toUpperCase()}
                                                    </div>
                                                    <div>
                                                        <h4 className="font-semibold text-slate-800 text-sm">{candidate.name}</h4>
                                                        <p className="text-xs text-slate-500">{candidate.position || 'No position'}</p>
                                                    </div>
                                                </div>
                                                {candidate.ai_score > 0 && (
                                                    <div className="flex items-center gap-1 text-amber-500">
                                                        <Sparkles className="w-3 h-3" />
                                                        <span className="text-xs font-semibold">{candidate.ai_score}</span>
                                                    </div>
                                                )}
                                            </div>

                                            <div className="flex items-center gap-2 text-xs text-slate-400 mb-3">
                                                <Mail className="w-3 h-3" />
                                                <span className="truncate">{candidate.email}</span>
                                            </div>

                                            {/* Status Change Dropdown */}
                                            <select
                                                value={candidate.status}
                                                onChange={(e) => handleStatusChange(candidate.id, e.target.value)}
                                                className="w-full text-xs border border-slate-200 rounded-lg px-2 py-1.5 bg-slate-50 focus:ring-2 focus:ring-blue-500"
                                            >
                                                <option value="applied">Applied</option>
                                                <option value="screening">Screening</option>
                                                <option value="interview">Interview</option>
                                                <option value="offer">Offer</option>
                                                <option value="hired">Hired</option>
                                                <option value="rejected">Rejected</option>
                                            </select>
                                        </motion.div>
                                    ))}
                                </AnimatePresence>

                                {getColumnCandidates(column.id).length === 0 && (
                                    <div className="h-24 flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-xl">
                                        <User className="w-5 h-5 mb-1" />
                                        <p className="text-xs font-medium">No candidates</p>
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
