// import React, { useEffect, useState } from 'react';
// import { Platform, PermissionsAndroid } from 'react-native';
// import PushNotification from 'react-native-push-notification'; // Replace with your chosen library (e.g., react-native-firebase)

// const NotificationComponent = () => {
//   const [scheduled, setScheduled] = useState(false);

//   useEffect(() => {
//     const scheduleNotification = async () => {
//       // Request notification permissions
//       if (Platform.OS === 'android') {
//         try {
//           const granted = await PermissionsAndroid.request(
//             PermissionsAndroid.PERMISSIONS.NOTIFICATION_ACCESS,
//             {
//               title: 'Push Notification Permission',
//               message: 'App needs notification permission to send reminders.',
//             }
//           );
//           if (granted !== PermissionsAndroid.RESULTS.GRANTED) {
//             console.warn('Notification permission denied (Android)');
//             return;
//           }
//         } catch (err) {
//           console.error('Error requesting notification permission (Android):', err);
//           return;
//         }
//       } else if (Platform.OS === 'ios') {
//         try {
//           // Request notification permission using UNUserNotificationCenter
//           const settings = await UNUserNotificationCenter.currentNotificationSettings();
//           if (settings.authorizationStatus !== UNAuthorizationStatus.Authorized) {
//             await UNUserNotificationCenter.requestAuthorizationAsync({
//               alert: true,
//               announcement: true,
//               badge: true,
//               sound: true,
//             });
//           }
//         } catch (err) {
//           console.error('Error requesting notification permission (iOS):', err);
//         }
//       }

//        // Schedule notifications for all four times
//        const times = [10, 15, 18, 21]; // Hours (adjust for 24-hour format if needed)
//        for (const time of times) {
//          try {
//            PushNotification.localNotificationSchedule({
//              channelId: 'your_channel_id', // Replace with your actual channel ID
//              title: 'Reminder',
//              message: `This is a reminder notification at ${time}:00!`,
//              vibrate: true,
//              allowWhileInForeground: true,
//              repeatType: 'day', // Repeat daily
//              repeatTime: (time - (new Date().getHours())) * 60 * 60 * 1000,
//            });
//          } catch (err) {
//            console.error('Error scheduling notification:', err);
//          }
//        }
//        setScheduled(true);
//      };
 
//      if (!scheduled) {
//        scheduleNotification();
//      }
//    }, [scheduled]); // Only schedule once
 
//    return (
//      <div>
//        {scheduled && <p>Notifications scheduled at 10AM, 3PM, 6PM, and 9PM!</p>}
//      </div>
//    );
//  };

// export default NotificationComponent;
