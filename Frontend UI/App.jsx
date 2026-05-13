import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard, Users, Package, TrendingUp, ShieldCheck, 
  ArrowRight, Globe, Zap, ShoppingBag, DollarSign, AlertTriangle, 
  ChevronRight, RefreshCw, Layers, Download, Cpu, Activity,
  Briefcase, Star, Search, Menu, X, Bell, User, Plus, CheckCircle2
} from 'lucide-react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, Cell, PieChart, Pie, LineChart, Line
} from 'recharts';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8001';

const App = () => {
  const [view, setView] = useState('landing');
  const [activeTab, setActiveTab] = useState('Neural Command');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [form, setForm] = useState({ order_id: '', category: 'Grocery', sub_category: '', product_name: '', sales: '', profit: '', quantity: '' });
  const [formStatus, setFormStatus] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isAiOpen, setIsAiOpen] = useState(false);
  const [chat, setChat] = useState([{ role: 'ai', text: 'Neural Strategy Link established. How can I assist your retail operations today?' }]);
  const [simParams, setSimParams] = useState({ priceAdj: 0, volAdj: 0, costAdj: 0 });

  const fetchAllData = async () => {
    setLoading(true);
    try {
      const summary = await axios.get(`${API_BASE}/api/summary`);
      const analytics = await axios.get(`${API_BASE}/api/analytics/full`);
      setData({ ...summary.data, ...analytics.data });
      setError(null);
    } catch (err) {
      console.error("API Error:", err);
      setError("Unable to connect to the Intelligence API. Ensure backend is running on port 8001.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (view === 'dashboard') fetchAllData();
  }, [view]);

  const handleExport = () => {
    const jsonString = `data:text/json;chatset=utf-8,${encodeURIComponent(
      JSON.stringify(data)
    )}`;
    const link = document.createElement("a");
    link.href = jsonString;
    link.download = "retail_intelligence_report.json";
    link.click();
  };

  const renderTabContent = (tab) => {
    if (!data) return null;
    
    switch(tab) {
      case 'Neural Command':
        return (
          <div className="space-y-10">
            <div className="grid grid-cols-4 gap-8">
              <StatCard label="Neural Volume" value={`$${(data.total_sales/1e6).toFixed(2)}M`} delta="+18.4%" icon={<DollarSign size={24}/>} color="blue" />
              <StatCard label="Net Yield" value={`$${(data.total_profit/1e3).toFixed(1)}K`} delta="+12.1%" icon={<TrendingUp size={24}/>} color="emerald" />
              <StatCard label="Global Orders" value={data.total_orders.toLocaleString()} delta="+9.5%" icon={<ShoppingBag size={24}/>} color="purple" />
              <StatCard label="Market Margin" value={`${(data.total_profit/data.total_sales*100).toFixed(1)}%`} delta="-1.2%" icon={<Layers size={24}/>} color="amber" />
            </div>
            
            <div className="grid grid-cols-3 gap-8">
              <div className="col-span-2 bg-[#0a0f24]/60 border border-white/5 rounded-[48px] p-12 backdrop-blur-xl relative overflow-hidden group">
                 <div className="absolute top-0 right-0 w-96 h-96 bg-blue-600/5 blur-[100px] rounded-full pointer-events-none" />
                 <div className="flex justify-between items-center mb-12">
                    <div>
                      <h3 className="text-2xl font-black font-outfit mb-1">Sales Performance Velocity</h3>
                      <p className="text-slate-500 text-sm font-bold uppercase tracking-widest">Global Tactical Sync</p>
                    </div>
                    <div className="flex gap-4">
                      <div className="flex items-center gap-2 text-xs font-bold text-slate-400"><div className="w-2 h-2 rounded-full bg-blue-600" /> Revenue</div>
                      <div className="flex items-center gap-2 text-xs font-bold text-slate-400"><div className="w-2 h-2 rounded-full bg-white/20" /> Projected</div>
                    </div>
                 </div>
                 <div className="h-[400px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data.trends}>
                      <defs>
                        <linearGradient id="gSales" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.5}/>
                          <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#ffffff05" vertical={false} />
                      <XAxis dataKey="Month" hide />
                      <YAxis hide />
                      <Tooltip 
                        contentStyle={{backgroundColor:'#0f172a', border:'1px solid rgba(255,255,255,0.1)', borderRadius:'24px', padding:'20px'}} 
                        itemStyle={{color:'#3b82f6', fontWeight:'900'}}
                      />
                      <Area type="monotone" dataKey="Sales" stroke="#3b82f6" strokeWidth={5} fill="url(#gSales)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
              
              <div className="bg-[#0a0f24]/60 border border-white/5 rounded-[48px] p-12 backdrop-blur-xl">
                 <h3 className="text-2xl font-black font-outfit mb-12">Category Architecture</h3>
                 <div className="h-[400px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={Object.entries(data.categories).map(([name, value]) => ({name, value}))} layout="vertical">
                        <YAxis dataKey="name" type="category" stroke="#475569" fontSize={12} width={100} axisLine={false} tickLine={false} />
                        <XAxis type="number" hide />
                        <Tooltip cursor={{fill:'rgba(255,255,255,0.05)'}} />
                        <Bar dataKey="value" radius={[0, 20, 20, 0]}>
                          {Object.entries(data.categories).map((e, i) => (
                            <Cell key={i} fill={e[0] === 'Grocery' ? '#fbbf24' : (i%2===0 ? '#3b82f6' : '#8b5cf6')} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                 </div>
                 <div className="mt-8 p-6 bg-amber-500/10 border border-amber-500/20 rounded-3xl flex items-center gap-4">
                    <div className="w-10 h-10 bg-amber-500 rounded-xl flex items-center justify-center"><Star size={20} fill="currentColor"/></div>
                    <div className="text-sm">
                      <span className="font-black text-amber-500 uppercase block tracking-widest text-[10px]">Insight Alert</span>
                      <span className="font-bold text-slate-300">Grocery segment (Flour) is trending 24% higher than Q1.</span>
                    </div>
                 </div>
              </div>
            </div>
          </div>
        );
      case 'Strategic Forecast':
        return (
          <div className="space-y-10">
            <div className="bg-blue-600/10 border-2 border-blue-600/20 p-12 rounded-[48px] relative overflow-hidden">
               <div className="absolute top-0 right-0 p-8 opacity-10"><TrendingUp size={200} /></div>
               <div className="relative z-10">
                  <h3 className="text-4xl font-black font-outfit mb-4 italic text-blue-500">Predictive Revenue Shift</h3>
                  <p className="text-xl text-slate-400 max-w-2xl font-light">Fourier-series decomposition shows a high-confidence growth trajectory for the next 6 neural cycles.</p>
               </div>
            </div>
            
            <div className="grid grid-cols-4 gap-8">
               <div className="col-span-3 bg-slate-900/40 border border-white/5 rounded-[48px] p-12">
                  <div className="h-[500px]">
                     <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={data.forecast}>
                           <CartesianGrid strokeDasharray="3 3" stroke="#ffffff05" />
                           <XAxis dataKey="Month" stroke="#475569" axisLine={false} tickLine={false} dy={10} />
                           <YAxis hide />
                           <Tooltip 
                              contentStyle={{backgroundColor:'#0f172a', border:'none', borderRadius:'24px'}}
                              labelStyle={{color:'#3b82f6', fontWeight:'900', marginBottom:'8px'}}
                           />
                           <Line type="monotone" dataKey="Predicted_Sales" stroke="#3b82f6" strokeWidth={6} dot={{r:8, fill:'#3b82f6', strokeWidth:4, stroke:'#0f172a'}} />
                        </LineChart>
                     </ResponsiveContainer>
                  </div>
               </div>
               <div className="space-y-8">
                  {[
                    {label: 'Forecast Confidence', value: '98.4%', sub: 'Based on 4yr Historicals'},
                    {label: 'Projected Revenue', value: '$2.4M', sub: 'Q3-Q4 Simulation'},
                    {label: 'Risk Variance', value: '±2.1%', sub: 'Market Volatility Index'}
                  ].map((item, i) => (
                    <div key={i} className="bg-white/5 border border-white/5 p-8 rounded-[40px] hover:border-blue-500/30 transition-all group">
                       <p className="text-xs font-black text-slate-500 uppercase tracking-widest mb-2">{item.label}</p>
                       <h4 className="text-4xl font-black font-outfit text-blue-500 group-hover:scale-105 transition-transform">{item.value}</h4>
                       <p className="text-[10px] font-bold text-slate-600 mt-2">{item.sub}</p>
                    </div>
                  ))}
               </div>
            </div>
          </div>
        );
      case 'Omnichannel':
        return (
          <div className="grid grid-cols-2 gap-8">
            <div className="bg-[#0a0f24]/60 border border-white/5 rounded-[48px] p-12 backdrop-blur-xl group hover:border-blue-500/20 transition-all">
               <h3 className="text-2xl font-black font-outfit mb-12">Revenue Distribution</h3>
               <div className="h-[450px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie data={data.omnichannel} dataKey="Sales" nameKey="Channel" cx="50%" cy="50%" innerRadius={120} outerRadius={170} paddingAngle={8}>
                        {data.omnichannel.map((e, i) => (
                          <Cell key={i} fill={['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b'][i % 4]} stroke="none" />
                        ))}
                      </Pie>
                      <Tooltip cursor={{fill:'transparent'}} contentStyle={{backgroundColor:'#0f172a', borderRadius:'24px'}} />
                    </PieChart>
                  </ResponsiveContainer>
               </div>
            </div>
            <div className="bg-[#0a0f24]/60 border border-white/5 rounded-[48px] p-12 backdrop-blur-xl group hover:border-emerald-500/20 transition-all">
               <h3 className="text-2xl font-black font-outfit mb-12">Channel Profit Efficiency</h3>
               <div className="h-[450px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data.omnichannel}>
                      <XAxis dataKey="Channel" stroke="#475569" axisLine={false} tickLine={false} />
                      <YAxis hide />
                      <Tooltip contentStyle={{backgroundColor:'#0f172a', borderRadius:'24px'}} />
                      <Bar dataKey="Profit" fill="#10b981" radius={[20, 20, 0, 0]}>
                         {data.omnichannel.map((e, i) => <Cell key={i} fill={e.Profit > 0 ? '#10b981' : '#ef4444'} />)}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
               </div>
            </div>
          </div>
        );
      case 'Inventory Engine':
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center mb-8">
               <h3 className="text-3xl font-black font-outfit italic">Stock Velocity Tracker</h3>
               <div className="flex gap-4">
                  <div className="px-6 py-2 rounded-xl bg-rose-500/10 text-rose-500 text-xs font-black uppercase tracking-widest border border-rose-500/20">Critical: 2 Items</div>
                  <div className="px-6 py-2 rounded-xl bg-emerald-500/10 text-emerald-500 text-xs font-black uppercase tracking-widest border border-emerald-500/20">Optimal: 15 Items</div>
               </div>
            </div>
            <div className="grid grid-cols-1 gap-4">
              {data.inventory.map((item, i) => (
                <motion.div 
                  key={i} 
                  initial={{opacity:0, x:-20}} 
                  animate={{opacity:1, x:0}} 
                  transition={{delay:i*0.05}}
                  className="bg-[#0a0f24]/60 border border-white/5 p-10 rounded-[32px] flex justify-between items-center group hover:border-blue-500/30 transition-all hover:bg-blue-600/[0.02]"
                >
                  <div className="flex items-center gap-8">
                    <div className={`w-16 h-16 rounded-2xl flex items-center justify-center font-black text-2xl ${item.Days_Left < 30 ? 'bg-rose-500/20 text-rose-500' : 'bg-blue-600/20 text-blue-600'}`}>
                      {item['Sub-Category'][0]}
                    </div>
                    <div>
                      <h4 className="text-2xl font-black mb-1 group-hover:text-blue-400 transition-colors">{item['Sub-Category']}</h4>
                      <p className="text-slate-500 font-bold uppercase tracking-widest text-[10px]">Global Inventory: <span className="text-slate-200">{item.Stock} Units</span></p>
                    </div>
                  </div>
                  <div className="flex items-center gap-16">
                     <div className="text-right">
                        <p className={`text-4xl font-black tracking-tighter ${item.Days_Left < 30 ? 'text-rose-500' : 'text-emerald-500'}`}>{item.Days_Left}d <span className="text-lg font-light text-slate-600">Left</span></p>
                        <div className="w-80 h-3 bg-slate-800/50 rounded-full mt-4 overflow-hidden border border-white/5">
                           <motion.div initial={{width:0}} animate={{width:`${Math.min(item.Days_Left, 100)}%`}} className={`h-full ${item.Days_Left < 30 ? 'bg-rose-500 shadow-[0_0_15px_#ef4444]' : 'bg-emerald-500 shadow-[0_0_15px_#10b981]'}`} />
                        </div>
                     </div>
                     <button className="w-14 h-14 rounded-2xl bg-white/5 flex items-center justify-center hover:bg-blue-600 hover:text-white transition-all">
                        <ArrowRight size={24} />
                     </button>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        );
      case 'Customer CLV':
        return (
          <div className="grid grid-cols-3 gap-10">
             <div className="bg-[#0a0f24]/60 border border-white/5 rounded-[48px] p-12">
                <h3 className="text-2xl font-black font-outfit mb-12">Segment Analysis</h3>
                <div className="h-[400px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie data={Object.entries(data.rfm.segments).map(([name, value]) => ({name, value}))} dataKey="value" nameKey="name" innerRadius={100} outerRadius={140} paddingAngle={5}>
                         {['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6'].map((c, i) => <Cell key={i} fill={c} stroke="none" />)}
                      </Pie>
                      <Tooltip contentStyle={{backgroundColor:'#0f172a', borderRadius:'24px'}} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="space-y-4 mt-8">
                   {Object.entries(data.rfm.segments).map(([name, val], i) => (
                     <div key={i} className="flex justify-between items-center p-4 bg-white/5 rounded-2xl">
                        <span className="font-bold text-slate-400">{name}</span>
                        <span className="font-black text-white">{val}</span>
                     </div>
                   ))}
                </div>
             </div>
             <div className="col-span-2 bg-[#0a0f24]/60 border border-white/5 rounded-[48px] p-12 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-8 opacity-5"><Users size={150} /></div>
                <h3 className="text-2xl font-black font-outfit mb-12">Top Strategic Assets <span className="text-slate-600 font-light ml-2">(Neural CLV Rank)</span></h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead>
                      <tr className="text-slate-500 text-[10px] font-black uppercase tracking-widest border-b border-white/5">
                        <th className="pb-8">Profile Identifier</th>
                        <th className="pb-8 text-right">Lifetime Volume</th>
                        <th className="pb-8 text-right">Loyalty Tier</th>
                        <th className="pb-8 text-right">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.rfm.top.map((c, i) => (
                        <tr key={i} className="border-b border-white/5 group hover:bg-blue-600/5 transition-all">
                          <td className="py-6 font-black text-lg flex items-center gap-4">
                             <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center text-xs group-hover:bg-blue-600 group-hover:text-white transition-all">{c['Customer ID'].slice(-2)}</div>
                             {c['Customer ID']}
                          </td>
                          <td className="py-6 text-right font-black text-emerald-400 text-xl">${c.Monetary.toFixed(0)}</td>
                          <td className="py-6 text-right">
                            <span className={`px-5 py-2 rounded-full text-[10px] font-black uppercase tracking-widest ${c.Segment === 'Platinum' ? 'bg-purple-600/20 text-purple-400' : 'bg-blue-600/20 text-blue-400'}`}>
                              {c.Segment}
                            </span>
                          </td>
                          <td className="py-6 text-right">
                             <div className="flex justify-end gap-1">
                                {[1,2,3,4,5].map(s => <Star key={s} size={10} fill={s <= 4 ? "#fbbf24" : "transparent"} stroke={s <= 4 ? "#fbbf24" : "#475569"} />)}
                             </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
             </div>
          </div>
        );
      case 'AI Fraud Audit':
        return (
          <div className="space-y-10">
            <div className="bg-rose-600/10 border-2 border-rose-500/20 p-12 rounded-[48px] flex items-center gap-12 relative overflow-hidden group">
               <div className="absolute top-0 right-0 p-12 opacity-10 group-hover:rotate-12 transition-transform duration-700"><ShieldCheck size={180} /></div>
               <div className="w-24 h-24 bg-rose-500 rounded-[32px] flex items-center justify-center shadow-3xl shadow-rose-600/40 transform -rotate-3"><AlertTriangle size={48} /></div>
               <div className="relative z-10">
                  <h4 className="text-4xl font-black font-outfit text-rose-500 mb-2 italic">Neural Fraud Audit Active</h4>
                  <p className="text-xl text-rose-400/70 font-light max-w-2xl">Isolation Forest (v4.2 Neural Core) has isolated 10 high-variance anomalies requiring tactical strategic review.</p>
               </div>
            </div>
            
            <div className="bg-[#0a0f24]/60 border border-white/5 rounded-[48px] overflow-hidden backdrop-blur-xl">
               <table className="w-full text-left">
                  <thead className="bg-white/5">
                     <tr className="text-slate-500 text-[10px] uppercase tracking-[0.3em] font-black">
                        <th className="p-10">Neural Sync Date</th>
                        <th>Operational Target</th>
                        <th className="text-right">Variance Volume</th>
                        <th className="text-right p-10">Strategic Status</th>
                     </tr>
                  </thead>
                  <tbody>
                     {data.anomalies.map((a, i) => (
                       <tr key={i} className="border-b border-white/5 hover:bg-rose-500/[0.03] transition-all group">
                          <td className="p-10 text-sm font-bold text-slate-500">{new Date(a['Order Date']).toLocaleDateString()}</td>
                          <td className="font-black text-lg group-hover:text-rose-400 transition-colors">{a['Customer Name']}</td>
                          <td className="text-right font-black text-rose-500 text-2xl">${a.Sales.toFixed(2)}</td>
                          <td className="text-right p-10">
                             <span className="px-6 py-3 bg-rose-500/20 text-rose-500 rounded-2xl text-xs font-black uppercase tracking-widest border border-rose-500/30">
                                Critical Flag
                             </span>
                          </td>
                       </tr>
                     ))}
                  </tbody>
               </table>
            </div>
          </div>
        );
      case 'Tactical Simulator':
        const originalProfit = data.total_profit;
        const originalSales = data.total_sales;
        const simulatedSales = originalSales * (1 + simParams.priceAdj/100) * (1 + simParams.volAdj/100);
        const simulatedProfit = simulatedSales * (originalProfit/originalSales) * (1 - simParams.costAdj/100);
        const profitDelta = ((simulatedProfit - originalProfit) / originalProfit * 100).toFixed(1);

        return (
          <div className="space-y-10">
             <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border-2 border-white/5 p-12 rounded-[48px] backdrop-blur-3xl">
                <h3 className="text-4xl font-black font-outfit mb-4 tracking-tighter">Neural Profit Simulator</h3>
                <p className="text-xl text-slate-400 font-light">Adjust tactical variables to simulate the impact on your bottom line.</p>
             </div>

             <div className="grid lg:grid-cols-3 gap-10">
                <div className="bg-slate-900/40 border border-white/5 p-10 rounded-[48px] space-y-10">
                   <h4 className="text-xl font-black uppercase tracking-widest text-blue-500">Variables</h4>
                   <SimSlider label="Price Adjustment" unit="%" min={-20} max={20} value={simParams.priceAdj} onChange={v => setSimParams({...simParams, priceAdj: v})} color="blue" />
                   <SimSlider label="Volume Variance" unit="%" min={-30} max={50} value={simParams.volAdj} onChange={v => setSimParams({...simParams, volAdj: v})} color="purple" />
                   <SimSlider label="Operational Cost" unit="%" min={-10} max={20} value={simParams.costAdj} onChange={v => setSimParams({...simParams, costAdj: v})} color="emerald" />
                </div>

                <div className="col-span-2 space-y-8">
                   <div className="grid grid-cols-2 gap-8">
                      <div className="bg-[#0a0f24]/80 border border-white/5 p-10 rounded-[48px] relative overflow-hidden">
                         <div className="text-xs font-black text-slate-500 uppercase tracking-widest mb-2">Simulated Net Profit</div>
                         <div className="text-5xl font-black font-outfit text-emerald-500">${(simulatedProfit/1e3).toFixed(1)}K</div>
                         <div className={`mt-4 inline-block px-3 py-1 rounded-full text-[10px] font-black ${parseFloat(profitDelta) >= 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}`}>
                            {parseFloat(profitDelta) >= 0 ? '+' : ''}{profitDelta}% Shift
                         </div>
                      </div>
                      <div className="bg-[#0a0f24]/80 border border-white/5 p-10 rounded-[48px]">
                         <div className="text-xs font-black text-slate-500 uppercase tracking-widest mb-2">Simulated Gross Volume</div>
                         <div className="text-5xl font-black font-outfit text-blue-500">${(simulatedSales/1e6).toFixed(2)}M</div>
                         <div className="mt-4 text-[10px] font-bold text-slate-500 italic">Projected Market Capture</div>
                      </div>
                   </div>

                   <div className="bg-[#0a0f24]/80 border border-white/5 p-10 rounded-[48px] h-[350px]">
                      <ResponsiveContainer width="100%" height="100%">
                         <BarChart data={[
                           {name: 'Current', Profit: originalProfit/1000, Sales: originalSales/10000},
                           {name: 'Simulated', Profit: simulatedProfit/1000, Sales: simulatedSales/10000}
                         ]}>
                            <XAxis dataKey="name" stroke="#475569" axisLine={false} tickLine={false} />
                            <Tooltip contentStyle={{backgroundColor:'#0f172a', borderRadius:'24px'}} />
                            <Bar dataKey="Profit" fill="#10b981" radius={[15, 15, 0, 0]} />
                            <Bar dataKey="Sales" fill="#3b82f6" radius={[15, 15, 0, 0]} />
                         </BarChart>
                      </ResponsiveContainer>
                   </div>
                </div>
             </div>
          </div>
        );
      case 'Add New Item':
        return (
          <div className="max-w-4xl mx-auto">
            <div className="bg-[#0a0f24]/60 border border-white/10 p-16 rounded-[48px] backdrop-blur-3xl relative overflow-hidden">
               <div className="absolute top-0 right-0 p-12 opacity-5"><Plus size={200} /></div>
               <h3 className="text-4xl font-black font-outfit mb-10 italic">Inject Tactical Data</h3>
               
               {formStatus && (
                 <motion.div initial={{opacity:0, y:-10}} animate={{opacity:1, y:0}} className="mb-8 p-6 bg-emerald-500/10 border border-emerald-500/20 rounded-3xl flex items-center gap-4 text-emerald-400 font-bold">
                    <CheckCircle2 size={24}/> {formStatus}
                 </motion.div>
               )}

               <div className="grid grid-cols-2 gap-8">
                  <div className="space-y-6">
                     <InputGroup label="Order ID" placeholder="e.g. CA-2024-001" value={form.order_id} onChange={e => setForm({...form, order_id: e.target.value})} />
                     <InputGroup label="Category" placeholder="e.g. Grocery" value={form.category} onChange={e => setForm({...form, category: e.target.value})} />
                     <InputGroup label="Sub-Category" placeholder="e.g. Flour" value={form.sub_category} onChange={e => setForm({...form, sub_category: e.target.value})} />
                  </div>
                  <div className="space-y-6">
                     <InputGroup label="Product Name" placeholder="e.g. Premium White Flour" value={form.product_name} onChange={e => setForm({...form, product_name: e.target.value})} />
                     <div className="grid grid-cols-2 gap-4">
                        <InputGroup label="Sales ($)" type="number" placeholder="0.00" value={form.sales} onChange={e => setForm({...form, sales: e.target.value})} />
                        <InputGroup label="Profit ($)" type="number" placeholder="0.00" value={form.profit} onChange={e => setForm({...form, profit: e.target.value})} />
                     </div>
                     <InputGroup label="Quantity" type="number" placeholder="1" value={form.quantity} onChange={e => setForm({...form, quantity: e.target.value})} />
                  </div>
               </div>

               <button 
                 onClick={async () => {
                   try {
                     await axios.post(`${API_BASE}/api/products/add`, {
                       ...form,
                       sales: parseFloat(form.sales),
                       profit: parseFloat(form.profit),
                       quantity: parseInt(form.quantity)
                     });
                     setFormStatus(`Successfully Added ${form.product_name}!`);
                     setTimeout(() => setFormStatus(null), 5000);
                     fetchAllData();
                   } catch (err) {
                     alert("Failed to add product. Check backend.");
                   }
                 }}
                 className="w-full mt-12 bg-blue-600 py-6 rounded-3xl font-black text-2xl shadow-3xl shadow-blue-600/40 hover:bg-blue-500 hover:-translate-y-1 transition-all"
               >
                 Synchronize to Mainframe
               </button>
            </div>
          </div>
        );
      default: return null;
    }
  };

  if (view === 'landing') {
    return (
      <div className="min-h-screen bg-[#020617] text-white selection:bg-blue-500/30 overflow-x-hidden">
        {/* Animated Background Gradients */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/10 blur-[120px] rounded-full animate-pulse" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/10 blur-[120px] rounded-full animate-pulse" style={{animationDelay: '2s'}} />
        </div>

        <nav className="flex justify-between items-center px-12 py-8 sticky top-0 z-50 backdrop-blur-xl border-b border-white/5">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center shadow-2xl shadow-blue-600/40 transform hover:rotate-12 transition-transform">
              <Zap size={28} fill="white" />
            </div>
            <span className="text-3xl font-black font-outfit tracking-tighter bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">RetailIntel Pro</span>
          </div>
          <div className="hidden md:flex gap-10 items-center font-bold text-slate-400">
            <a href="#platform" className="hover:text-white transition-all hover:scale-110">Intelligence</a>
            <a href="#predictions" className="hover:text-white transition-all hover:scale-110">AI Models</a>
            <a href="#enterprise" className="hover:text-white transition-all hover:scale-110">Enterprise</a>
            <button onClick={() => setView('dashboard')} className="bg-white text-black px-10 py-4 rounded-2xl font-black hover:scale-105 transition-all active:scale-95 shadow-2xl shadow-white/10 group">
              Launch Neural Suite
              <ArrowRight className="inline-block ml-2 group-hover:translate-x-1 transition-transform" size={20}/>
            </button>
          </div>
        </nav>

        <header id="platform" className="px-12 py-32 max-w-7xl mx-auto grid lg:grid-cols-2 gap-20 items-center relative z-10">
          <motion.div initial={{opacity:0, x:-50}} animate={{opacity:1, x:0}} transition={{duration:0.8}}>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-black mb-8 uppercase tracking-widest animate-bounce">
              <Star size={14} fill="currentColor" />
              v4.5 Neural Architecture
            </div>
            <h1 className="text-[6rem] font-black font-outfit leading-[0.85] mb-8 tracking-tighter">
              Retail <br/><span className="text-blue-500 italic">Synchronized.</span>
            </h1>
            <p className="text-2xl text-slate-400 leading-relaxed mb-12 max-w-xl font-light">
              Orchestrate your global retail empire with <span className="text-white font-bold">Predictive Intelligence</span>. Transform raw data into strategic dominance.
            </p>
            <div className="flex flex-wrap gap-6">
              <button onClick={() => setView('dashboard')} className="bg-blue-600 px-12 py-6 rounded-3xl font-black text-xl flex items-center gap-4 shadow-3xl shadow-blue-600/40 hover:bg-blue-500 hover:-translate-y-1 transition-all">
                Access Intelligence <Cpu size={24}/>
              </button>
              <button className="border-2 border-white/10 px-12 py-6 rounded-3xl font-bold text-xl hover:bg-white/5 hover:border-white/20 transition-all">
                Watch Demo
              </button>
            </div>
          </motion.div>
          <motion.div initial={{opacity:0, scale:0.8}} animate={{opacity:1, scale:1}} transition={{duration:1}} className="relative group">
             <div className="absolute inset-0 bg-blue-600/30 blur-[150px] rounded-full animate-pulse" />
             <div className="relative bg-[#0a0f24]/80 border-2 border-white/10 rounded-[64px] p-12 backdrop-blur-3xl shadow-3xl transform group-hover:scale-[1.02] transition-all duration-700">
                <div className="flex justify-between items-center mb-10">
                  <div className="flex gap-2">
                    <div className="w-3 h-3 rounded-full bg-rose-500" />
                    <div className="w-3 h-3 rounded-full bg-amber-500" />
                    <div className="w-3 h-3 rounded-full bg-emerald-500" />
                  </div>
                  <div className="text-xs font-black text-slate-500 tracking-widest uppercase">Neural Analytics Live</div>
                </div>
                <div className="h-96 bg-slate-900/50 rounded-3xl border border-white/5 flex items-end p-10 gap-4 overflow-hidden relative">
                   <div className="absolute top-8 left-8">
                      <div className="text-4xl font-black tracking-tighter text-blue-500">+42.8%</div>
                      <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mt-1">AI Projected Growth</div>
                   </div>
                   {[70, 45, 95, 65, 88, 50, 80, 55, 90, 75, 85].map((h, i) => (
                     <motion.div 
                       key={i} 
                       initial={{height:0}} 
                       animate={{height:`${h}%`}} 
                       transition={{delay:i*0.1, duration:1, ease:"easeOut"}} 
                       className="flex-1 bg-gradient-to-t from-blue-600 to-violet-600 rounded-t-2xl relative group/bar"
                     >
                       <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-white text-black text-[10px] font-black px-2 py-1 rounded opacity-0 group-hover/bar:opacity-100 transition-opacity whitespace-nowrap">
                         VAL: {h}%
                       </div>
                     </motion.div>
                   ))}
                </div>
             </div>
          </motion.div>
        </header>

        <section id="predictions" className="px-12 py-40 bg-white/[0.02] relative">
           <div className="max-w-7xl mx-auto">
              <div className="text-center mb-32">
                <h2 className="text-6xl font-black font-outfit mb-6 tracking-tighter">Strategic Intelligence Matrix</h2>
                <p className="text-xl text-slate-500 max-w-2xl mx-auto">Propel your operational efficiency with our multi-layered AI audit systems.</p>
              </div>
              <div className="grid lg:grid-cols-3 gap-10">
                 <FeatureCard 
                   icon={<Globe className="text-blue-500" size={48}/>}
                   title="Omnichannel Sync"
                   desc="Unified neural bridge across e-commerce, mobile applications, and global physical storefronts."
                   color="blue"
                 />
                 <FeatureCard 
                   icon={<Package className="text-emerald-500" size={48}/>}
                   title="Predictive Logistics"
                   desc="Advanced restock triggers driven by Fourier-transform seasonality models and local demand shifts."
                   color="emerald"
                 />
                 <FeatureCard 
                   icon={<ShieldCheck className="text-rose-500" size={48}/>}
                   title="Neural Fraud Audit"
                   desc="Real-time Isolation Forest anomaly detection securing every tactical transaction in your network."
                   color="rose"
                 />
              </div>
           </div>
        </section>

        <footer id="enterprise" className="py-32 text-center border-t border-white/5 relative overflow-hidden">
           <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-px bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-30" />
           <h2 className="text-5xl font-black font-outfit mb-8 tracking-tighter italic">Ready for the Neural Shift?</h2>
           <p className="text-slate-500 text-xl mb-12 font-light">Join the elite global retailers orchestrating their future today.</p>
           <button onClick={() => setView('dashboard')} className="bg-white text-black px-16 py-6 rounded-full font-black text-2xl hover:scale-110 transition-all shadow-3xl shadow-white/10 active:scale-95">
             Enterprise Onboarding
           </button>
        </footer>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#020617] text-white flex font-inter overflow-hidden">
      {/* Sidebar */}
      <aside className={`bg-[#070b1d] border-r border-white/5 flex flex-col p-8 sticky top-0 h-screen transition-all duration-500 z-50 ${isSidebarOpen ? 'w-80' : 'w-24'}`}>
        <div className="flex items-center gap-4 mb-16 overflow-hidden">
          <div className="min-w-[48px] h-12 bg-blue-600 rounded-2xl flex items-center justify-center shadow-xl shadow-blue-600/30">
            <Zap size={24} fill="currentColor"/>
          </div>
          {isSidebarOpen && <span className="text-2xl font-black font-outfit tracking-tighter whitespace-nowrap">RetailIntel</span>}
        </div>
        
        <nav className="flex-1 space-y-3 overflow-y-auto pr-2 custom-scrollbar">
          {[
            {label: 'Neural Command', icon: <Activity size={20}/>},
            {label: 'Strategic Forecast', icon: <TrendingUp size={20}/>},
            {label: 'Omnichannel', icon: <Globe size={20}/>},
            {label: 'Inventory Engine', icon: <Package size={20}/>},
            {label: 'Customer CLV', icon: <Users size={20}/>},
            {label: 'AI Fraud Audit', icon: <ShieldCheck size={20}/>},
            {label: 'Tactical Simulator', icon: <Cpu size={20}/>},
            {label: 'Add New Item', icon: <Plus size={20}/>}
          ].map(item => (
            <div 
              key={item.label}
              onClick={() => setActiveTab(item.label)}
              className={`flex items-center gap-4 px-5 py-4 rounded-2xl cursor-pointer transition-all duration-300 font-bold group ${activeTab === item.label ? 'bg-blue-600 text-white shadow-2xl shadow-blue-600/40' : 'text-slate-500 hover:bg-white/5 hover:text-slate-200'}`}
            >
              <div className="group-hover:scale-125 transition-transform">{item.icon}</div>
              {isSidebarOpen && <span className="whitespace-nowrap">{item.label}</span>}
            </div>
          ))}
        </nav>

        <div className="mt-auto space-y-4">
          <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="flex items-center gap-4 text-slate-600 hover:text-blue-400 transition-all font-bold w-full">
            <div className="w-10 h-10 rounded-xl bg-slate-800/30 flex items-center justify-center">{isSidebarOpen ? <X size={20}/> : <Menu size={20}/>}</div>
            {isSidebarOpen && <span>Minimize View</span>}
          </button>
          <button onClick={() => setView('landing')} className="flex items-center gap-4 text-slate-600 hover:text-rose-400 transition-all font-bold group w-full">
            <div className="w-10 h-10 rounded-xl bg-slate-800/30 flex items-center justify-center group-hover:bg-rose-500/20"><Layers size={20}/></div>
            {isSidebarOpen && <span>Exit Suite</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative bg-gradient-to-br from-[#020617] to-[#0a0f24]">
        {/* Top Floating Header */}
        <header className="p-8 flex justify-between items-center sticky top-0 z-40 backdrop-blur-3xl bg-[#020617]/40 border-b border-white/5">
          <div className="flex items-center gap-6">
            <div className="relative group">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-500 transition-colors" size={18} />
              <input 
                type="text" 
                placeholder="Search neural records..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-white/5 border border-white/5 rounded-2xl pl-12 pr-6 py-3 w-80 focus:w-96 focus:border-blue-500/50 outline-none transition-all font-bold placeholder:text-slate-600"
              />
            </div>
            <div className="h-10 w-px bg-white/5 hidden md:block" />
            <div className="hidden lg:flex gap-4">
               <div className="px-4 py-2 rounded-xl bg-white/5 border border-white/5 flex items-center gap-2 text-xs font-bold text-slate-400">
                  <Activity size={14} className="text-blue-500" />
                  API Lateny: 12ms
               </div>
               <div className="px-4 py-2 rounded-xl bg-white/5 border border-white/5 flex items-center gap-2 text-xs font-bold text-slate-400">
                  <Cpu size={14} className="text-purple-500" />
                  Compute: 84%
               </div>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="relative group">
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-rose-500 rounded-full border-2 border-[#020617] flex items-center justify-center text-[8px] font-black">2</div>
              <button className="p-4 rounded-2xl bg-slate-900/50 border border-white/5 hover:bg-slate-800 transition-all">
                <Bell size={20} />
              </button>
            </div>
            <button onClick={handleExport} className="p-4 rounded-2xl bg-blue-600/10 border border-blue-500/20 text-blue-400 hover:bg-blue-600 hover:text-white transition-all group">
              <Download size={20} className="group-hover:-translate-y-1 transition-transform" />
            </button>
            <button onClick={fetchAllData} className="p-4 rounded-2xl bg-slate-900/50 border border-white/5 hover:bg-slate-800 transition-all">
              <RefreshCw size={20} className={loading ? 'animate-spin' : ''} />
            </button>
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-slate-700 to-slate-900 border border-white/10 flex items-center justify-center cursor-pointer hover:border-blue-500/50 transition-all">
               <User size={24} />
            </div>
          </div>
        </header>

        <div className="p-10 max-w-[1600px] mx-auto">
          {error ? (
            <motion.div initial={{opacity:0, scale:0.95}} animate={{opacity:1, scale:1}} className="bg-rose-500/5 border-2 border-rose-500/20 p-16 rounded-[48px] text-center backdrop-blur-2xl">
              <div className="w-24 h-24 bg-rose-500/20 rounded-full flex items-center justify-center mx-auto mb-8 animate-pulse">
                <AlertTriangle className="text-rose-500" size={48} />
              </div>
              <h3 className="text-4xl font-black font-outfit text-rose-500 mb-4">Neural Connection Severed</h3>
              <p className="text-xl text-rose-400/60 mb-10 max-w-lg mx-auto">{error}</p>
              <button onClick={fetchAllData} className="bg-rose-600 px-12 py-5 rounded-3xl font-black text-xl shadow-2xl shadow-rose-600/30 hover:bg-rose-500 transition-all active:scale-95">Restart Link</button>
            </motion.div>
          ) : loading ? (
            <div className="space-y-10">
               <div className="grid grid-cols-4 gap-8">
                  {[1,2,3,4].map(i => <div key={i} className="h-48 bg-white/5 rounded-[40px] animate-pulse" />)}
               </div>
               <div className="grid grid-cols-3 gap-8">
                  <div className="col-span-2 h-[500px] bg-white/5 rounded-[40px] animate-pulse" />
                  <div className="h-[500px] bg-white/5 rounded-[40px] animate-pulse" />
               </div>
            </div>
          ) : (
            <AnimatePresence mode="wait">
              <motion.div 
                key={activeTab} 
                initial={{opacity:0, y:20, filter: 'blur(10px)'}} 
                animate={{opacity:1, y:0, filter: 'blur(0px)'}} 
                exit={{opacity:0, y:-20, filter: 'blur(10px)'}}
                transition={{duration:0.5, ease: "circOut"}}
              >
                {renderTabContent(activeTab)}
              </motion.div>
            </AnimatePresence>
          )}
        </div>
        
        {/* Floating AI Assistant */}
        <div className="fixed bottom-10 right-10 z-[100]">
           <AnimatePresence>
              {isAiOpen && (
                <motion.div 
                  initial={{opacity:0, scale:0.9, y:20}}
                  animate={{opacity:1, scale:1, y:0}}
                  exit={{opacity:0, scale:0.9, y:20}}
                  className="bg-[#0f172a] border border-white/10 w-96 h-[500px] rounded-[40px] mb-6 shadow-3xl backdrop-blur-3xl overflow-hidden flex flex-col"
                >
                   <div className="p-6 bg-blue-600 flex justify-between items-center">
                      <div className="flex items-center gap-3">
                         <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center"><Cpu size={16}/></div>
                         <span className="font-black text-sm">Neural Assistant</span>
                      </div>
                      <button onClick={() => setIsAiOpen(false)}><X size={20}/></button>
                   </div>
                   <div className="flex-1 p-6 space-y-4 overflow-y-auto">
                      {chat.map((m, i) => (
                        <div key={i} className={`flex ${m.role === 'ai' ? 'justify-start' : 'justify-end'}`}>
                           <div className={`max-w-[80%] p-4 rounded-2xl text-sm font-bold ${m.role === 'ai' ? 'bg-white/5 text-slate-300' : 'bg-blue-600 text-white'}`}>
                              {m.text}
                           </div>
                        </div>
                      ))}
                   </div>
                   <div className="p-6 border-t border-white/5 flex gap-2">
                      <input 
                        className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-xs outline-none focus:border-blue-500/50" 
                        placeholder="Ask strategy..." 
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' && e.target.value) {
                            const val = e.target.value;
                            setChat([...chat, {role: 'user', text: val}, {role: 'ai', text: 'Analyzing market vectors... Recommendation: Optimize "Grocery" margins by 5.2% based on current velocity.'}]);
                            e.target.value = '';
                          }
                        }}
                      />
                   </div>
                </motion.div>
              )}
           </AnimatePresence>
           <button 
             onClick={() => setIsAiOpen(!isAiOpen)}
             className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center shadow-3xl shadow-blue-600/40 hover:scale-110 active:scale-95 transition-all group"
           >
              <Cpu className="text-white group-hover:rotate-12 transition-transform" size={32}/>
           </button>
        </div>
      </main>
    </div>
  );
};

const FeatureCard = ({ icon, title, desc, color }) => (
  <div className={`p-12 rounded-[48px] bg-white/[0.03] border border-white/5 hover:border-${color}-500/30 transition-all duration-500 group relative overflow-hidden`}>
    <div className={`absolute -top-24 -right-24 w-48 h-48 bg-${color}-600/10 blur-[80px] rounded-full group-hover:scale-150 transition-transform duration-1000`} />
    <div className="mb-8 p-6 bg-white/5 rounded-3xl inline-block group-hover:scale-110 group-hover:bg-blue-600/20 transition-all duration-500">{icon}</div>
    <h3 className="text-3xl font-black font-outfit mb-4 group-hover:translate-x-2 transition-transform">{title}</h3>
    <p className="text-slate-400 text-lg leading-relaxed">{desc}</p>
  </div>
);

const InputGroup = ({ label, placeholder, value, onChange, type="text" }) => (
  <div className="space-y-2">
    <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-2">{label}</label>
    <input 
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      className="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 focus:border-blue-500/50 outline-none transition-all font-bold placeholder:text-slate-700"
    />
  </div>
);

const SimSlider = ({ label, value, onChange, min, max, unit, color }) => (
  <div className="space-y-4">
    <div className="flex justify-between items-center">
       <span className="text-sm font-bold text-slate-400">{label}</span>
       <span className={`font-black text-blue-500`}>{value > 0 ? '+' : ''}{value}{unit}</span>
    </div>
    <input 
      type="range" 
      min={min} 
      max={max} 
      value={value} 
      onChange={(e) => onChange(parseInt(e.target.value))}
      className={`w-full h-2 bg-white/5 rounded-full appearance-none cursor-pointer accent-blue-600`}
    />
    <div className="flex justify-between text-[8px] font-black text-slate-700 uppercase tracking-tighter">
       <span>{min}{unit}</span>
       <span>Neutral</span>
       <span>{max}{unit}</span>
    </div>
  </div>
);

const StatCard = ({ label, value, delta, icon, color }) => {
  const colors = {
    blue: 'text-blue-500 bg-blue-500/10 hover:bg-blue-600',
    emerald: 'text-emerald-500 bg-emerald-500/10 hover:bg-emerald-600',
    purple: 'text-purple-500 bg-purple-500/10 hover:bg-purple-600',
    amber: 'text-amber-500 bg-amber-500/10 hover:bg-amber-600'
  };
  
  return (
    <div className="bg-[#0a0f24]/60 border border-white/10 p-10 rounded-[48px] backdrop-blur-2xl hover:border-blue-500/40 transition-all duration-500 group cursor-default relative overflow-hidden">
      <div className="flex justify-between items-start mb-8 relative z-10">
         <div className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-all duration-500 group-hover:rotate-12 group-hover:text-white ${colors[color] || colors.blue}`}>{icon}</div>
         <span className={`text-[10px] font-black px-3 py-1.5 rounded-full uppercase tracking-widest ${delta.startsWith('+') ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'}`}>{delta}</span>
      </div>
      <p className="text-slate-500 text-[10px] font-black mb-1 uppercase tracking-[0.2em] relative z-10">{label}</p>
      <h4 className="text-4xl font-black font-outfit tracking-tighter relative z-10 group-hover:translate-x-1 transition-transform">{value}</h4>
    </div>
  );
};

export default App;
