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

export function formatTimeString(timeStr : string) {
  const [hours, minutes, seconds] = timeStr.split(':').map(Number);
  let parts = [];

  if (hours > 0) parts.push(`${hours} hour${hours !== 1 ? 's' : ''}`);
  if (minutes > 0) parts.push(`${minutes} minute${minutes !== 1 ? 's' : ''}`);
  if (seconds > 0) parts.push(`${seconds} second${seconds !== 1 ? 's' : ''}`);

  return parts.length > 1 ? parts.slice(0, -1).join(', ') + ' and ' + parts.slice(-1) : parts[0] || '0 seconds';
}