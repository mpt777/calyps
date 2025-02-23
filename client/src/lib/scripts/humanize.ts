export function fractionalize(floatValue : number) {
  const tolerance = 1.0e-2;

  const wholePart = Math.floor(floatValue);
  const fractionalPart = floatValue - wholePart;

  for (let denominator = 1; denominator <= 100; denominator++) {
      const numerator = Math.round(fractionalPart * denominator);
      const difference = Math.abs(fractionalPart - (numerator / denominator));

      if (difference < tolerance) {
          if (numerator === 0) {
              return wholePart.toString();
          } else {
              return `${wholePart || ""} ${numerator}/${denominator}`;
          }
      }
  }
}

export function pluralize(word:string, value : number, suffix:string="s") {
  return value === 1 ? `${word}` : `${word}${suffix}`;
}

export function formatTimeString(seconds : number) {
  const hours = Math.floor(seconds / 3600); // 1 hour = 3600 seconds
  const minutes = Math.floor((seconds % 3600) / 60); // 1 minute = 60 seconds
  
  let result = '';
  
  if (hours > 0) {
      result += `${hours} hour${hours !== 1 ? 's' : ''}`;
  }
  
  if (minutes > 0) {
      if (result.length > 0) result += ' and ';
      result += `${minutes} min${minutes !== 1 ? 's' : ''}`;
  }
  
  if (result === '') {
      result = '0 mins'; // If no hours or minutes, just return 0 minutes
  }
  
  return result;
}

export function generateHandle(name: string) {
  return (name || "")
      .toLowerCase()                    // Convert to lowercase
      .replace(/\s+/g, '-')              // Replace spaces with hyphens
      .replace(/[^\w\-]+/g, '')          // Remove non-alphanumeric characters except hyphens
      .replace(/--+/g, '-')              // Replace multiple hyphens with a single hyphen
    //   .replace(/^-+/, '')                // Remove leading hyphens
    //   .replace(/-+$/, '');               // Remove trailing hyphens
}