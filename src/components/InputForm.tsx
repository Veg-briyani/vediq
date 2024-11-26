// src/components/InputForm.tsx
import { useFormValidation } from '@/hooks/useFormValidation';

export default function InputForm({ onSubmit }: { onSubmit: (data: BirthData) => void }) {
 const [formData, setFormData] = useState({
   date: "",
   time: "",
   latitude: "",
   longitude: ""
 });
 
 const [errors, setErrors] = useState<Record<string, string>>({});
 const { validateBirthData } = useFormValidation();

 const handleSubmit = (e: React.FormEvent) => {
   e.preventDefault();
   const validationErrors = validateBirthData(formData);
   
   if (Object.keys(validationErrors).length === 0) {
     onSubmit({
       date: formData.date,
       time: formData.time,
       latitude: parseFloat(formData.latitude),
       longitude: parseFloat(formData.longitude)
     });
   } else {
     setErrors(validationErrors);
   }
 };

 return (
   <form onSubmit={handleSubmit} className="space-y-4">
     <div>
       <label className="block text-sm font-medium mb-1">Date of Birth</label>
       <input
         type="date"
         value={formData.date}
         onChange={e => setFormData({...formData, date: e.target.value})}
         className={`w-full rounded-md ${errors.date ? 'border-red-500' : 'border-gray-300'}`}
       />
       {errors.date && <p className="text-red-500 text-sm mt-1">{errors.date}</p>}
     </div>

     <div>
       <label className="block text-sm font-medium mb-1">Time of Birth</label>
       <input
         type="time"
         value={formData.time}
         onChange={e => setFormData({...formData, time: e.target.value})}
         className={`w-full rounded-md ${errors.time ? 'border-red-500' : 'border-gray-300'}`}
       />
       {errors.time && <p className="text-red-500 text-sm mt-1">{errors.time}</p>}
     </div>

     <div>
       <label className="block text-sm font-medium mb-1">Latitude</label>
       <input
         type="number"
         step="any"
         value={formData.latitude}
         onChange={e => setFormData({...formData, latitude: e.target.value})}
         className={`w-full rounded-md ${errors.latitude ? 'border-red-500' : 'border-gray-300'}`}
         placeholder="-90 to 90"
       />
       {errors.latitude && <p className="text-red-500 text-sm mt-1">{errors.latitude}</p>}
     </div>

     <div>
       <label className="block text-sm font-medium mb-1">Longitude</label>
       <input
         type="number"
         step="any"
         value={formData.longitude}
         onChange={e => setFormData({...formData, longitude: e.target.value})}
         className={`w-full rounded-md ${errors.longitude ? 'border-red-500' : 'border-gray-300'}`}
         placeholder="-180 to 180"
       />
       {errors.longitude && <p className="text-red-500 text-sm mt-1">{errors.longitude}</p>}
     </div>

     <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-md">
       Calculate Chart
     </button>
   </form>
 );
}