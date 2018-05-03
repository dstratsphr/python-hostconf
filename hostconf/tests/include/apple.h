/*
 * HA!  Not *Apple* Inc.
 */

#define HONEYCRISP 1
#define GALA       2
#define DELICIOUS  3

typedef struct _apple {
    int   seed_count;
    int   sweetness;
    char *variety;
} apple_t;


int pick_apple();
