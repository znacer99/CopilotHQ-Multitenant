import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, Check, X, Clock, AlertCircle } from 'lucide-react';
import api from '../lib/api';
import { cn } from '../lib/utils';

interface LeaveRequest {
    id: number;
    employee_email: string;
    leave_type: string;
    start_date: string;
    end_date: string;
    days_requested: number;
    reason: string;
    status: 'pending' | 'approved' | 'rejected';
    created_at: string;
}

const LEAVE_TYPES = [
    { value: 'annual', label: 'Annual Leave', color: 'bg-blue-100 text-blue-700' },
    { value: 'sick', label: 'Sick Leave', color: 'bg-red-100 text-red-700' },
    { value: 'personal', label: 'Personal Leave', color: 'bg-purple-100 text-purple-700' },
    { value: 'maternity', label: 'Maternity Leave', color: 'bg-pink-100 text-pink-700' },
    { value: 'paternity', label: 'Paternity Leave', color: 'bg-cyan-100 text-cyan-700' },
    { value: 'unpaid', label: 'Unpaid Leave', color: 'bg-gray-100 text-gray-700' },
];

export default function Leave() {
    const [requests, setRequests] = useState<LeaveRequest[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [filter, setFilter] = useState<'all' | 'pending' | 'approved' | 'rejected'>('all');

    useEffect(() => {
        fetchRequests();
    }, []);

    const fetchRequests = async () => {
        try {
            const response = await api.get('/leave-requests/');
            setRequests(response.data);
        } catch (error) {
            console.error("Failed to fetch leave requests", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleStatusChange = async (requestId: number, newStatus: 'approved' | 'rejected') => {
        try {
            await api.patch(`/leave-requests/${requestId}/`, {
                status: newStatus,
                reviewed_at: new Date().toISOString()
            });
            fetchRequests();
        } catch (error) {
            console.error("Failed to update status", error);
        }
    };

    const filteredRequests = filter === 'all'
        ? requests
        : requests.filter(r => r.status === filter);

    const pendingCount = requests.filter(r => r.status === 'pending').length;

    const getLeaveTypeStyle = (type: string) => {
        return LEAVE_TYPES.find(t => t.value === type)?.color || 'bg-gray-100 text-gray-700';
    };

    if (isLoading) return <div className="p-8">Loading leave requests...</div>;

    return (
        <div className="h-full flex flex-col">
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Leave Management</h1>
                    <p className="text-slate-500 mt-1">Review and manage leave requests</p>
                </div>
                {pendingCount > 0 && (
                    <div className="flex items-center gap-2 bg-amber-50 border border-amber-200 text-amber-700 px-4 py-2 rounded-xl">
                        <AlertCircle className="w-5 h-5" />
                        <span className="font-medium">{pendingCount} pending requests</span>
                    </div>
                )}
            </div>

            {/* Filter Tabs */}
            <div className="flex gap-2 mb-6">
                {(['all', 'pending', 'approved', 'rejected'] as const).map(tab => (
                    <button
                        key={tab}
                        onClick={() => setFilter(tab)}
                        className={cn(
                            "px-4 py-2 rounded-lg font-medium text-sm transition-colors capitalize",
                            filter === tab
                                ? "bg-blue-600 text-white"
                                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                        )}
                    >
                        {tab}
                    </button>
                ))}
            </div>

            {/* Request List */}
            <div className="flex-1 overflow-auto">
                <div className="space-y-4">
                    <AnimatePresence>
                        {filteredRequests.map(request => (
                            <motion.div
                                key={request.id}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow"
                            >
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-3 mb-2">
                                            <h3 className="font-semibold text-slate-800">{request.employee_email}</h3>
                                            <span className={cn("px-2.5 py-0.5 rounded-full text-xs font-medium", getLeaveTypeStyle(request.leave_type))}>
                                                {LEAVE_TYPES.find(t => t.value === request.leave_type)?.label}
                                            </span>
                                            <span className={cn(
                                                "px-2.5 py-0.5 rounded-full text-xs font-medium",
                                                request.status === 'pending' && "bg-amber-100 text-amber-700",
                                                request.status === 'approved' && "bg-green-100 text-green-700",
                                                request.status === 'rejected' && "bg-red-100 text-red-700"
                                            )}>
                                                {request.status}
                                            </span>
                                        </div>

                                        <div className="flex items-center gap-4 text-sm text-slate-500 mb-2">
                                            <div className="flex items-center gap-1">
                                                <Calendar className="w-4 h-4" />
                                                <span>{request.start_date} → {request.end_date}</span>
                                            </div>
                                            <div className="flex items-center gap-1">
                                                <Clock className="w-4 h-4" />
                                                <span>{request.days_requested} day(s)</span>
                                            </div>
                                        </div>

                                        {request.reason && (
                                            <p className="text-sm text-slate-600 mt-2 p-3 bg-slate-50 rounded-lg">
                                                "{request.reason}"
                                            </p>
                                        )}
                                    </div>

                                    {request.status === 'pending' && (
                                        <div className="flex gap-2 ml-4">
                                            <button
                                                onClick={() => handleStatusChange(request.id, 'approved')}
                                                className="p-2 bg-green-100 text-green-700 hover:bg-green-200 rounded-lg transition-colors"
                                                title="Approve"
                                            >
                                                <Check className="w-5 h-5" />
                                            </button>
                                            <button
                                                onClick={() => handleStatusChange(request.id, 'rejected')}
                                                className="p-2 bg-red-100 text-red-700 hover:bg-red-200 rounded-lg transition-colors"
                                                title="Reject"
                                            >
                                                <X className="w-5 h-5" />
                                            </button>
                                        </div>
                                    )}
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {filteredRequests.length === 0 && (
                        <div className="h-48 flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-2xl">
                            <Calendar className="w-8 h-8 mb-2" />
                            <p className="font-medium">No leave requests found</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
