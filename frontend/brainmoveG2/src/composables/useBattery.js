import { computed } from 'vue';
import { BatteryMedium, BatteryFull, BatteryLow } from 'lucide-vue-next';

export function useBattery(batteryPercentage) {
    const isLowBattery = computed(() => {
        return batteryPercentage.value < 25;
    });

    const batteryIcon = computed(() => {
        if (batteryPercentage.value >= 75) {
            return BatteryFull;
        } else if (batteryPercentage.value >= 25) {
            return BatteryMedium;
        } else {
            return BatteryLow;
        }
    });

    return {
        isLowBattery,
        batteryIcon
    };
}
