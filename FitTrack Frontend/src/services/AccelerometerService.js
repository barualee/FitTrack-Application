import { Accelerometer } from 'expo-sensors';

// Constants for the high-pass filter
const ALPHA = 0.8;
let lastX, lastY, lastZ;

export const startAccelerometer = (callback) => {
  const subscription = Accelerometer.addListener(({ x, y, z }) => {
    // Initialize last values if not set
    if (!lastX && !lastY && !lastZ) {
      lastX = x;
      lastY = y;
      lastZ = z;
      return;
    }

    // Apply high-pass filter to remove gravity component
    let filteredX = ALPHA * (lastX - x);
    let filteredY = ALPHA * (lastY - y);
    let filteredZ = ALPHA * (lastZ - z);

    lastX = x;
    lastY = y;
    lastZ = z;

    // Call the callback function with filtered data
    callback({ x: filteredX, y: filteredY, z: filteredZ });
     //callback({ x, y, z });
  });

  return subscription;
};

export const stopAccelerometer = (subscription) => {
  subscription && subscription.remove();
};

