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