/**
 * Drawing grid in rectangular coordinates
 *
 * e.g. alignment of your chart?
 */
export default function Grid(props = {}) {
  return {
    top: 30,
    bottom: 20,
    left: '3%',
    right: '3%',
    containLabel: true,
    ...props,
  };
}
