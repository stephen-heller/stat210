#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stddef.h>
#include <time.h>

/**
 * Randomly generates a sequence of length seq_len, up to 64 long, with 
 * 1's and 0's denoting successes/failures. Return value is a 64 bit integer,
 * the first seq_len bits of which denote the sequence. Success rate is a percentage, 
 * expressed as a scale of 0-100 (e.g. 50)
 */
uint64_t generate_sequence(size_t seq_len, double success_rate) {
    uint64_t sequence = 0;

    for (int i = 0; i < seq_len; ++i) {

        if (rand() % 100 < success_rate) {
            sequence |= (1ULL << i); // if successful shot, set that bit to 1
        }
    }

    return sequence;

}
/**
 * Runs the simulation for num_trials trials, with seq_len and sucess rate as parameters. Outputs
 * The average success rate after a streak each as a number between 0 and 1, or as -1 if no streaks occur
 * during that trial.
 */
void run_sim(size_t num_trials, size_t seq_len, double success_rate, double* output_results) {

    srand(time(NULL));

    uint64_t streak_mask = (1ULL << 3) - 1; // 0b111
    uint64_t full_window_mask = (1ULL << 4) - 1; // 0b1111
    uint64_t success_pattern = (1ULL << 3) | streak_mask;

    for (size_t i = 0; i < num_trials; i++) {
        uint64_t sequence = generate_sequence(seq_len, success_rate);
        
        int num_streaks = 0;
        int successes_after_streak = 0;

        for (int shift = 0; shift <= 50 - 4; shift++) {
            uint64_t window = (num_streaks >> shift) & full_window_mask;

            if ((window & streak_mask) == streak_mask) {
                num_streaks++;
                if (window == success_pattern) {
                    successes_after_streak++;
                }
            }
        }

        if (num_streaks == 0) {
            output_results[i] = -1.0;
        } 
        else {
            output_results[i] = (double)successes_after_streak / num_streaks;
        }
    }
}

