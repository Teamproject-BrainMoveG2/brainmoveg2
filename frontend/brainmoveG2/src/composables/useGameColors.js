import { computed } from 'vue';

/**
 * Composable for getting game-specific colors and button classes
 * @param {Ref<string>} gameId - The game ID as a ref
 * @returns {Object} - Color utilities for the game
 */
export function useGameColors(gameId) {
    // Map game IDs to color variants
    const colorVariant = computed(() => {
        const colorMap = {
            '1': 'green',
            '2': 'orange',
            '3': 'primary',
            '4': 'purple'
        };
        return colorMap[gameId.value] || 'primary'; // Default to primary (blue)
    });

    // Get the button class based on game ID
    const buttonClass = computed(() => {
        return `c-btn c-btn--${colorVariant.value}`;
    });

    // Get background colors for cards
    const cardBackgroundColor = computed(() => {
        const backgroundMap = {
            '1': 'var(--accent-green-light)',
            '2': 'var(--accent-orange-light)',
            '3': 'var(--primary-light)',
            '4': 'var(--purple-light)'
        };
        return backgroundMap[gameId.value] || 'var(--primary-light)';
    });

    // Get primary colors
    const primaryColor = computed(() => {
        const primaryMap = {
            '1': 'var(--accent-green)',
            '2': 'var(--accent-orange)',
            '3': 'var(--primary)',
            '4': 'var(--purple)'
        };
        return primaryMap[gameId.value] || 'var(--primary)';
    });

    return {
        colorVariant,
        buttonClass,
        cardBackgroundColor,
        primaryColor
    };
}
