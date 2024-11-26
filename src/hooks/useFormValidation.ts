// src/hooks/useFormValidation.ts
export function useFormValidation() {
    const validateBirthData = (data: {
      date: string,
      time: string,
      latitude: string,
      longitude: string
    }) => {
      const errors: Record<string, string> = {};
  
      if (!data.date) {
        errors.date = 'Birth date is required';
      }
      if (!data.time) {
        errors.time = 'Birth time is required';
      }
      
      const lat = parseFloat(data.latitude);
      if (isNaN(lat) || lat < -90 || lat > 90) {
        errors.latitude = 'Invalid latitude (-90 to 90)';
      }
      
      const lng = parseFloat(data.longitude);
      if (isNaN(lng) || lng < -180 || lng > 180) {
        errors.longitude = 'Invalid longitude (-180 to 180)';
      }
  
      return errors;
    };
  
    return { validateBirthData };
  }