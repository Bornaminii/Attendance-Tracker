import { Text, View } from "react-native";

export function HomeScreen() {
  return (
    <View className="flex-1 items-center justify-center bg-white px-6">
      <Text className="text-2xl font-semibold text-slate-900">Attendance Tracker</Text>
      <Text className="mt-2 text-center text-slate-500">
        Teacher workspace shell. Sign-in arrives in the next phases.
      </Text>
    </View>
  );
}
