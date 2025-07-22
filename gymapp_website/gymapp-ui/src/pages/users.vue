<template>
    <v-container fluid>
        <v-row justify="center" align="center" v-if="!userStore.isLoggedIn">
            <v-col cols="12" md="6">
                <v-card justify="center" align="center">
                    <v-card-title>Login / Sign Up</v-card-title>
                    <v-card-text>
                        <v-text-field
                            v-model="returningUser.username"
                            label="Username"
                            :loading="loading"
                        ></v-text-field>
                        <v-text-field
                            v-model="returningUser.password"
                            label="Password"
                            :rules="[passwordRules.required, passwordRules.min]"
                            :append-inner-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                            :type="show ? 'text' : 'password'"
                            :hint="'At least 8 characters' & passwordRules.min"
                            class="input-group--focused"
                            @click:append-inner="show = !show"
                            :loading="loading"
                        ></v-text-field>
                        <v-card-actions>
                            <v-btn @click="signupDialog = true" color="primary">Sign Up</v-btn>
                            <v-spacer></v-spacer>
                            <v-btn @click="loginUser" color="success">Login</v-btn>
                        </v-card-actions>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        
        <!-- User Dashboard when logged in -->
        <v-row v-else>
            <v-col cols="12">
                <v-card>
                    <v-card-title class="d-flex justify-space-between align-center">
                        <span>Welcome back, {{ userStore.fullName }}!</span>
                        <div>
                            <v-btn
                                v-if="!editMode"
                                @click="enableEditMode"
                                color="primary"
                                prepend-icon="mdi-pencil"
                            >
                                Edit Profile
                            </v-btn>
                            <v-btn
                                v-else
                                @click="cancelEdit"
                                color="grey"
                                class="mr-2"
                            >
                                Cancel
                            </v-btn>
                            <v-btn
                                v-if="editMode"
                                @click="saveProfile"
                                color="success"
                                prepend-icon="mdi-content-save"
                                :loading="saving"
                            >
                                Save Changes
                            </v-btn>
                        </div>
                    </v-card-title>
                    <v-card-text>
                        <v-form ref="profileForm" v-model="formValid">
                            <v-row>
                                <!-- Personal Information Section -->
                                <v-col cols="12" md="6">
                                    <v-text-field
                                        v-model="editedUser.username"
                                        label="Username"
                                        :readonly="true"
                                        disabled
                                        prepend-icon="mdi-account"
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <v-text-field
                                        v-model="editedUser.email"
                                        label="Email"
                                        :readonly="!editMode"
                                        :rules="editMode ? [rules.email] : []"
                                        prepend-icon="mdi-email"
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <v-text-field
                                        v-model="editedUser.first_name"
                                        label="First Name"
                                        :readonly="!editMode"
                                        :rules="editMode ? [rules.required] : []"
                                        prepend-icon="mdi-account-edit"
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <v-text-field
                                        v-model="editedUser.last_name"
                                        label="Last Name"
                                        :readonly="!editMode"
                                        :rules="editMode ? [rules.required] : []"
                                    ></v-text-field>
                                </v-col>
                                
                                <!-- Physical Information Section -->
                                <v-col cols="12" md="3">
                                    <v-text-field
                                        v-model.number="editedUser.age"
                                        label="Age"
                                        type="number"
                                        :readonly="!editMode"
                                        :rules="editMode ? [rules.required, rules.age] : []"
                                        prepend-icon="mdi-calendar"
                                        suffix="years"
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12" md="3">
                                    <v-select
                                        v-model="editedUser.sex"
                                        :items="sexOptions"
                                        label="Sex"
                                        :readonly="!editMode"
                                        prepend-icon="mdi-gender-male-female"
                                    ></v-select>
                                </v-col>
                                <v-col cols="12" md="3">
                                    <v-text-field
                                        v-if="!editMode"
                                        :model-value="formatHeight(editedUser.height)"
                                        label="Height"
                                        readonly
                                        prepend-icon="mdi-human-male-height"
                                    ></v-text-field>
                                    <div v-else class="d-flex align-center">
                                        <v-text-field
                                            v-model.number="height_ft"
                                            type="number"
                                            label="ft"
                                            :rules="[rules.required, rules.heightFt]"
                                            class="mr-2"
                                            hide-details
                                        ></v-text-field>
                                        <v-text-field
                                            v-model.number="height_in"
                                            type="number"
                                            label="in"
                                            :rules="[rules.required, rules.heightIn]"
                                            hide-details
                                        ></v-text-field>
                                    </div>
                                </v-col>
                                <v-col cols="12" md="3">
                                    <v-text-field
                                        v-model.number="editedUser.weight"
                                        label="Weight"
                                        type="number"
                                        :readonly="!editMode"
                                        :rules="editMode ? [rules.required, rules.weight] : []"
                                        prepend-icon="mdi-weight"
                                        suffix="lbs"
                                    ></v-text-field>
                                </v-col>
                                
                                <!-- Fitness Information Section -->
                                <v-col cols="12" md="6">
                                    <v-text-field
                                        v-model.number="editedUser.experience"
                                        label="Years of Experience"
                                        type="number"
                                        :readonly="!editMode"
                                        :rules="editMode ? [rules.required, rules.experience] : []"
                                        prepend-icon="mdi-dumbbell"
                                        suffix="years"
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <v-text-field
                                        v-model="editedUser.last_use"
                                        label="Last Workout Date"
                                        type="date"
                                        :readonly="!editMode"
                                        prepend-icon="mdi-calendar-check"
                                    ></v-text-field>
                                </v-col>
                                
                                <!-- Goals Section with Chips -->
                                <v-col cols="12">
                                    <v-select
                                        v-model="editedUser.goal"
                                        :items="goalOptions"
                                        label="Fitness Goals"
                                        multiple
                                        chips
                                        closable-chips
                                        :readonly="!editMode"
                                        prepend-icon="mdi-target"
                                        :rules="editMode ? [rules.goals] : []"
                                    >
                                        <template v-slot:chip="{ props, item }">
                                            <v-chip
                                                v-bind="props"
                                                :color="getGoalColor(item.value)"
                                                text-color="white"
                                                :closable="editMode"
                                            >
                                                {{ item.title }}
                                            </v-chip>
                                        </template>
                                    </v-select>
                                </v-col>
                                
                                <!-- Password Change Section (only in edit mode) -->
                                <v-col cols="12" v-if="editMode">
                                    <v-expansion-panels>
                                        <v-expansion-panel>
                                            <v-expansion-panel-title>
                                                <v-icon class="mr-2">mdi-lock-reset</v-icon>
                                                Change Password
                                            </v-expansion-panel-title>
                                            <v-expansion-panel-text>
                                                <v-row>
                                                    <v-col cols="12" md="6">
                                                        <v-text-field
                                                            v-model="passwordChange.new"
                                                            label="New Password"
                                                            :type="showNewPassword ? 'text' : 'password'"
                                                            :append-inner-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                                            @click:append-inner="showNewPassword = !showNewPassword"
                                                            :rules="passwordChange.new ? [passwordRules.min] : []"
                                                        ></v-text-field>
                                                    </v-col>
                                                    <v-col cols="12" md="6">
                                                        <v-text-field
                                                            v-model="passwordChange.confirm"
                                                            label="Confirm New Password"
                                                            :type="showConfirmPassword ? 'text' : 'password'"
                                                            :append-inner-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                                            @click:append-inner="showConfirmPassword = !showConfirmPassword"
                                                            :rules="passwordChange.confirm ? [passwordMatch] : []"
                                                        ></v-text-field>
                                                    </v-col>
                                                </v-row>
                                            </v-expansion-panel-text>
                                        </v-expansion-panel>
                                    </v-expansion-panels>
                                </v-col>
                            </v-row>
                        </v-form>
                    </v-card-text>
                </v-card>
                
                <!-- Quick Stats Card -->
                <v-card class="mt-4">
                    <v-card-title>
                        <v-icon left>mdi-chart-line</v-icon>
                        Quick Stats
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols="12" md="3">
                                <v-card flat color="primary" dark>
                                    <v-card-text class="text-center">
                                        <div class="text-h4">{{ calculateBMI() }}</div>
                                        <div>BMI</div>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols="12" md="3">
                                <v-card flat color="success" dark>
                                    <v-card-text class="text-center">
                                        <div class="text-h4">{{ editedUser.experience }}</div>
                                        <div>Years Training</div>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols="12" md="3">
                                <v-card flat color="info" dark>
                                    <v-card-text class="text-center">
                                        <div class="text-h4">{{ editedUser.goal.length }}</div>
                                        <div>Active Goals</div>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols="12" md="3">
                                <v-card flat color="warning" dark>
                                    <v-card-text class="text-center">
                                        <div class="text-h4">{{ daysSinceLastWorkout() }}</div>
                                        <div>Days Since Last Workout</div>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        
        <!-- Sign Up Dialog -->
        <v-dialog v-model="signupDialog" max-width="800px">
            <v-card>
                <v-card-title>Create New Account</v-card-title>
                <v-card-text>
                    <v-row justify="center" align="center">
                        <v-col cols="12" md="6">
                            <v-text-field
                                v-model="new_user.username"
                                label="Username"
                                required
                                density="compact"
                                :loading="loading"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6">
                            <v-text-field
                                v-model="new_user.password"
                                label="Password"
                                :rules="[passwordRules.required, passwordRules.min]"
                                :type="show ? 'text' : 'password'"
                                :append-inner-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                                @click:append-inner="show = !show"
                                density="compact"
                                :loading="loading"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row justify="center" align="center">
                        <v-col cols="12" md="6">
                            <v-text-field
                                v-model="new_user.first_name"
                                label="First Name"
                                density="compact"
                                :loading="loading"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6">
                            <v-text-field
                                v-model="new_user.last_name"
                                label="Last Name"
                                density="compact"
                                :loading="loading"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row justify="center" align="center">
                        <v-col cols="12" md="6">
                            <v-text-field
                                v-model="new_user.email"
                                label="Email"
                                density="compact"
                                :loading="loading"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="3">
                            <div class="d-flex align-center">
                                <v-text-field
                                    v-model.number="new_user.height_ft"
                                    type="number"
                                    label="Height (ft)"
                                    variant="outlined"
                                    density="compact"
                                    :min="0"
                                    :max="8"
                                    :loading="loading"
                                    class="mr-2"
                                ></v-text-field>
                                <span class="mr-4">ft</span>
                                <v-text-field
                                    v-model.number="new_user.height_in"
                                    type="number"
                                    label="Height (in)"
                                    variant="outlined"
                                    density="compact"
                                    :min="0"
                                    :max="11"
                                    :loading="loading"
                                    class="mr-2"
                                ></v-text-field>
                                <span>in</span>
                            </div>
                        </v-col>
                    </v-row>
                    <v-row justify="center" align="center">
                        <v-col cols="12" md="2">
                            <v-text-field
                                v-model="new_user.weight"
                                label="Weight (lbs)"
                                density="compact"
                                :loading="loading"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2">
                            <v-text-field
                                v-model="new_user.age"
                                label="Age"
                                density="compact"
                                :loading="loading"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2">
                            <v-select
                                v-model="new_user.sex"
                                :items="sexOptions"
                                label="Sex"
                                density="compact"
                                :loading="loading"
                            ></v-select>
                        </v-col>
                    </v-row>
                    <v-row justify="center" align="center">
                        <v-col cols="12" md="3">
                            <v-text-field
                                v-model.number="new_user.experience"
                                type="number"
                                label="Years of Experience"
                                density="compact"
                                :min="0"
                                :loading="loading"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="3">
                            <v-text-field
                                v-model.date="new_user.last_use"
                                type="date"
                                label="Date of Last Workout"
                                density="compact"
                                :loading="loading"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="4">
                            <v-select
                                v-model="new_user.goal"
                                :items="goalOptions"
                                multiple
                                chips
                                label="Fitness Goal"
                                density="compact"
                                :loading="loading"
                            ></v-select>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-card-actions>
                    <v-btn @click="signupDialog = false" color="primary">Cancel</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn @click="createUser" color="success">Sign Up</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        
        <v-snackbar
            v-model="snackbar"
            :color="snackbarColor"
            :timeout="3000"
        >
            {{ snackbarText }}
        </v-snackbar>
    </v-container>
</template>

<script>
import ApiRequests from '@/api/request';
import { useUserStore } from '@/stores/user';

export default {
    name: 'userInfo',
    
    components: {
    },

    setup() {
        const userStore = useUserStore()
        
        userStore.initializeAuth()
        
        return { userStore }
    },

    data() {
        return {
            new_user: {
                username: null,
                password: null,
                first_name: null,
                last_name: null,
                email: null,
                sex: null,
                age: null,
                height: null,
                height_ft: null,
                height_in: null,
                weight: null,
                last_use: null,
                experience: null,
                goal: [],
            },
            editedUser: {},
            editMode: false,
            formValid: true,
            saving: false,
            loading: false,
            passwordRules: {
                required: value => !!value || 'Required.',
                min: v => (v && v.length >= 8) || 'Min 8 characters',
            },
            rules: {
                required: v => !!v || 'This field is required',
                email: v => !v || /.+@.+\..+/.test(v) || 'Email must be valid',
                age: v => (v && v >= 10 && v <= 100) || 'Age must be between 10 and 100',
                weight: v => (v && v >= 50 && v <= 500) || 'Weight must be between 50 and 500 lbs',
                experience: v => (v >= 0 && v <= 50) || 'Experience must be between 0 and 50 years',
                heightFt: v => (v >= 3 && v <= 8) || 'Height must be between 3 and 8 feet',
                heightIn: v => (v >= 0 && v <= 11) || 'Inches must be between 0 and 11',
                goals: v => (v && v.length > 0) || 'Select at least one goal'
            },
            height_ft: null,
            height_in: null,
            passwordChange: {
                new: '',
                confirm: ''
            },
            showNewPassword: false,
            showConfirmPassword: false,
            returningUser: {
                username: null,
                password: null,
            },
            signupDialog: false,
            show: false,
            snackbar: false,
            snackbarText: '',
            snackbarColor: 'success',
            sexOptions: ['Male', 'Female', 'Other'],
            goalOptions: [
                'Bulk', 
                'Cut', 
                'General Fitness', 
                'Lean Muscle Gain', 
                'Maintenance', 
                'Muscle Gain', 
                'Strength', 
                'Tone', 
                'Weight Loss'
            ]
        };
    },
    
    computed: {
        passwordMatch() {
            return this.passwordChange.new === this.passwordChange.confirm || 'Passwords must match'
        }
    },
    
    watch: {
        'userStore.currentUser': {
            handler(newUser) {
                if (newUser) {
                    this.editedUser = { ...newUser };
                    if (this.editedUser.height) {
                        this.height_ft = Math.floor(this.editedUser.height / 12);
                        this.height_in = this.editedUser.height % 12;
                    }
                }
            },
            immediate: true,
            deep: true
        }
    },

    mounted() {
        if (this.$route.query.tab === 'login' && !this.userStore.isLoggedIn) {
            this.activeTab = 0;
        }
    },

    methods: {
        async loginUser() {
            if (!this.returningUser.username || !this.returningUser.password) {
                this.showSnackbar('Please enter username and password', 'error');
                return;
            }
            
            this.loading = true;
            const result = await this.userStore.login(this.returningUser);
            this.loading = false;
            
            if (result.success) {
                this.showSnackbar('Login successful!', 'success');
                this.returningUser = { username: null, password: null };
            } else {
                this.showSnackbar(result.error || 'Login failed', 'error');
            }
        },

        async createUser() {
            if (!this.new_user.username || !this.new_user.password) {
                this.showSnackbar('Username and password are required', 'error');
                return;
            }
            
            this.new_user.height = (this.new_user.height_ft * 12) + this.new_user.height_in;
            
            if (!this.new_user.last_use) {
                this.new_user.last_use = new Date().toISOString();
            }
            
            this.loading = true;
            const result = await this.userStore.signup(this.new_user);
            this.loading = false;
            
            if (result.success) {
                this.showSnackbar('Account created successfully!', 'success');
                this.signupDialog = false;
                this.resetNewUser();
            } else {
                this.showSnackbar(result.error || 'Signup failed', 'error');
            }
        },
        
        enableEditMode() {
            this.editMode = true;
            this.editedUser = { ...this.userStore.currentUser };
            if (this.editedUser.height) {
                this.height_ft = Math.floor(this.editedUser.height / 12);
                this.height_in = this.editedUser.height % 12;
            }
        },
        
        cancelEdit() {
            this.editMode = false;
            this.editedUser = { ...this.userStore.currentUser };
            this.passwordChange = { new: '', confirm: '' };
            this.showNewPassword = false;
            this.showConfirmPassword = false;
        },
        
        async saveProfile() {
            const valid = await this.$refs.profileForm.validate();
            if (!valid.valid) {
                this.showSnackbar('Please fix the errors in the form', 'error');
                return;
            }
            
            this.saving = true;
            
            try {
                if (this.height_ft !== null && this.height_in !== null) {
                    this.editedUser.height = (this.height_ft * 12) + this.height_in;
                }
                
                const updateData = {
                    first_name: this.editedUser.first_name,
                    last_name: this.editedUser.last_name,
                    age: this.editedUser.age,
                    height: this.editedUser.height,
                    weight: this.editedUser.weight,
                    sex: this.editedUser.sex,
                    experience: this.editedUser.experience,
                    last_use: this.editedUser.last_use,
                    goal: this.editedUser.goal
                };
                
                if (this.passwordChange.new && this.passwordChange.new === this.passwordChange.confirm) {
                    updateData.password = this.passwordChange.new;
                }
                
                const response = await ApiRequests.updateUser(this.userStore.currentUser.item_id, updateData);
                
                this.userStore.updateUserData(response.data);
                
                this.showSnackbar('Profile updated successfully!', 'success');
                this.editMode = false;
                this.passwordChange = { new: '', confirm: '' };
                
            } catch (error) {
                console.error('Error updating profile:', error);
                this.showSnackbar(error.response?.data?.detail || 'Failed to update profile', 'error');
            } finally {
                this.saving = false;
            }
        },
        
        formatHeight(inches) {
            if (!inches) return 'Not set';
            const feet = Math.floor(inches / 12);
            const remainingInches = inches % 12;
            return `${feet}' ${remainingInches}"`;
        },
        
        calculateBMI() {
            if (!this.editedUser.weight || !this.editedUser.height) return 'N/A';
            const bmi = (this.editedUser.weight / (this.editedUser.height * this.editedUser.height)) * 703;
            return bmi.toFixed(1);
        },
        
        daysSinceLastWorkout() {
            if (!this.editedUser.last_use) return 'N/A';
            const lastWorkout = new Date(this.editedUser.last_use);
            const today = new Date();
            const diffTime = Math.abs(today - lastWorkout);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            return diffDays;
        },
        
        getGoalColor(goal) {
            const colors = {
                'Bulk': 'purple',
                'Cut': 'orange',
                'General Fitness': 'blue',
                'Lean Muscle Gain': 'green',
                'Maintenance': 'grey',
                'Muscle Gain': 'red',
                'Strength': 'brown',
                'Tone': 'pink',
                'Weight Loss': 'yellow'
            };
            return colors[goal] || 'primary';
        },

        resetNewUser() {
            this.new_user = {
                username: null,
                password: null,
                first_name: null,
                last_name: null,
                email: null,
                sex: null,
                age: null,
                height: null,
                height_ft: null,
                height_in: null,
                weight: null,
                last_use: null,
                experience: null,
                goal: [],
            };
        },

        showSnackbar(text, color = 'success') {
            this.snackbarText = text;
            this.snackbarColor = color;
            this.snackbar = true;
        }
    }
};
</script>

<style scoped>
.v-chip {
    margin: 2px;
}

.v-expansion-panel {
    margin-top: 16px;
}
</style>