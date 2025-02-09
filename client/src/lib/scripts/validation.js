export function formatZodError(errors) {
  const formatted = {};
  console.log(errors, "ERRORS")

  errors.forEach(error => {
      let current = formatted;
      error.path.forEach((key, index) => {
          if (index === error.path.length - 1) {
              current[key] = error.message;
          } else {
              current[key] = current[key] || {};
              current = current[key];
          }
      });
  });

  return formatted;
}

export const getDefaults = (schema) => {
    const defaults = {};
    for (const key in schema.shape) {
        const field = schema.shape[key];
        if (field._def.defaultValue) {
        defaults[key] = field._def.defaultValue();
        }
    }
    return defaults;
    }