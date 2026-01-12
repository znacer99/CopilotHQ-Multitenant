import { motion } from 'framer-motion';
import { Users, UserPlus, Clock, TrendingUp } from 'lucide-react';
import { cn } from '../lib/utils';

const StatCard = ({ title, value, change, icon: Icon, color }: any) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow"
    >
        <div className="flex items-center justify-between mb-4">
            <div className={cn("p-3 rounded-xl", color)}>
                <Icon className="w-6 h-6 text-white" />
            </div>
            <span className={cn("text-sm font-medium px-2.5 py-1 rounded-full",
                change.startsWith('+') ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
            )}>
                {change}
            </span>
        </div>
        <h3 className="text-slate-500 text-sm font-medium">{title}</h3>
        <p className="text-2xl font-bold text-slate-800 mt-1">{value}</p>
    </motion.div>
);

export default function Dashboard() {
    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl font-bold text-slate-800">Dashboard</h1>
                <p className="text-slate-500 mt-1">Welcome back, John. Here's what's happening today.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Total Employees"
                    value="124"
                    change="+12%"
                    icon={Users}
                    color="bg-blue-500"
                />
                <StatCard
                    title="New Hires"
                    value="8"
                    change="+4%"
                    icon={UserPlus}
                    color="bg-purple-500"
                />
                <StatCard
                    title="Pending Leave"
                    value="12"
                    change="-2%"
                    icon={Clock}
                    color="bg-amber-500"
                />
                <StatCard
                    title="Retention Rate"
                    value="98.2%"
                    change="+1.2%"
                    icon={TrendingUp}
                    color="bg-emerald-500"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm h-[400px] flex items-center justify-center text-slate-400">
                    Chart Placeholder: Employee Growth
                </div>
                <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm h-[400px] flex items-center justify-center text-slate-400">
                    Chart Placeholder: Department Distribution
                </div>
            </div>
        </div>
    );
}
