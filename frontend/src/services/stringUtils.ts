export function snakeToCamel(str: string): string {
  return str.replace(/([_]\w)/g, (g) => g[1].toUpperCase());
}

export function camelToSnake(str: string): string {
  return str.replace(/([A-Z])/g, (group) => '_' + group.toLowerCase());
}

export function isObject(o: any): o is Record<string, object> {
  return o === Object(o) && !Array.isArray(o) && typeof o !== 'function';
}

export function keysToCamel(o: object): object {
  if (Array.isArray(o)) {
    return o.map((i) => {
      return keysToCamel(i);
    });
  } else if (isObject(o)) {
    const n: Record<string, object> = {};

    Object.keys(o).forEach((k) => {
      n[snakeToCamel(k)] = keysToCamel(o[k]);
    });

    return n;
  }

  return o;
}

export function keysToSnake(o: object): object {
  if (isObject(o)) {
    const n: Record<string, object> = {};

    Object.keys(o).forEach((k) => {
      n[camelToSnake(k)] = keysToSnake(o[k]);
    });

    return n;
  } else if (Array.isArray(o)) {
    return o.map((i) => {
      return keysToSnake(i);
    });
  }

  return o;
}
