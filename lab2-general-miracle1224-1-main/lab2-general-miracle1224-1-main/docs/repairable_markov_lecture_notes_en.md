# Repairable System Computation Notes (Instructor Version)
## Topic: Full-State Markov Model and Steady-State Availability

---

## 1. Class Objectives

By the end of this session, each student must be able to:

1. Write the repairable single-component model and derive steady-state availability.
2. Explain the relation between the full-state Markov model and the steady-state approximation method.
3. Compute component and system availability from lab data and complete basic validation checks.

---

## 2. Symbols and Conventions

Use the following notation consistently:

- Failure rate: $\lambda$, unit $\mathrm{h}^{-1}$
- Repair rate: $\mu$, unit $\mathrm{h}^{-1}$
- Duty cycle: $duty$
- Effective failure rate: $\lambda_{eff}=\lambda\cdot duty$
- Component steady-state availability: $A_i$
- System steady-state availability: $A_{sys}$

Default lab convention:

$$
A_i=\frac{\mu_i}{\lambda_{eff,i}+\mu_i}
$$

---

## 3. Core Derivations

### 1. Single-Component Two-State Markov Model

States:

- $U$: up (operational)
- $D$: down (failed)

Transition rates:

- $U\to D$: $\lambda$
- $D\to U$: $\mu$

Steady-state balance:

$$
\pi_U\lambda=\pi_D\mu,\quad \pi_U+\pi_D=1
$$

Hence:

$$
\pi_U=\frac{\mu}{\lambda+\mu}
$$

Therefore:

$$
A=\frac{\mu}{\lambda+\mu}
$$

With duty-cycle correction:

$$
\lambda_{eff}=\lambda\cdot duty,\quad
A=\frac{\mu}{\lambda_{eff}+\mu}
$$

### 2. Two-Component Full-State Model (Demonstration)

Let both components be repairable. Define states:

- $S_0=(U,U)$
- $S_1=(D,U)$
- $S_2=(U,D)$
- $S_3=(D,D)$

Generator matrix:

$$
Q=\begin{bmatrix}
-(\lambda_1+\lambda_2) & \lambda_1 & \lambda_2 & 0\\
\mu_1 & -(\mu_1+\lambda_2) & 0 & \lambda_2\\
\mu_2 & 0 & -(\mu_2+\lambda_1) & \lambda_1\\
0 & \mu_2 & \mu_1 & -(\mu_1+\mu_2)
\end{bmatrix}
$$

Steady-state equations:

$$
\pi Q=0,\quad \sum_{k=0}^3\pi_k=1
$$

Interpretation:

- Series system: $A_{sys}=\pi_0$
- Parallel system (1oo2): $A_{sys}=1-\pi_3$

---

## 4. Calculation Procedure Used in the Lab

### Step 1: Compute duty cycle from mission profile

For each component:

$$
duty_i=\frac{\text{total active time of component }i}{\text{total cycle time}}
$$

### Step 2: Compute effective failure rate

$$
\lambda_{eff,i}=\lambda_i\cdot duty_i
$$

### Step 3: Compute component availability

$$
A_i=\frac{\mu_i}{\lambda_{eff,i}+\mu_i}
$$

### Step 4: Compute system availability

Treat each $A_i$ as the edge availability in `model.json`, then compute source-target connectivity availability as $A_{sys}$.

---

## 5. Worked Example

Given a component:

- $\lambda=8.0\times10^{-5}\ \mathrm{h}^{-1}$
- $duty=0.35$
- $\mu=0.25\ \mathrm{h}^{-1}$

### 1. Compute $\lambda_{eff}$

$$
\lambda_{eff}=8.0\times10^{-5}\times0.35=2.8\times10^{-5}\ \mathrm{h}^{-1}
$$

### 2. Compute steady-state availability

$$
A=\frac{0.25}{0.25+2.8\times10^{-5}}
=\frac{0.25}{0.250028}
\approx 0.999888
$$

Conclusion: long-run availability is approximately $99.9888\%$.

---

## 6. Structural Combination Example

Assume:

- Series components: $A_1=0.9990,\ A_2=0.9980$
- Parallel components: $A_3=0.9970,\ A_4=0.9960$

Parallel block:

$$
A_{34}=1-(1-A_3)(1-A_4)
=1-(0.0030)(0.0040)=0.999988
$$

If system is " $A_1,A_2$ in series, then in series with the parallel block":

$$
A_{sys}=A_1A_2A_{34}
=0.9990\times0.9980\times0.999988
\approx 0.9970
$$

---

## 7. Mandatory Report Content

### Task 3 (Repairable system) must include:

1. Convention statement (whether $\lambda_{eff}$ is used).
2. At least one full hand-calculation of component $A_i$.
3. System $A_{sys}$ and engineering interpretation.

### Task 4 (Analysis) must include:

1. Which component/path is weakest.
2. Why it is weak (both parameter and topology reasons).
3. At least one improvement action with expected direction ( $A_{sys}$ increase).

---

## 8. Validation Rules

You must verify:

1. If a key component repair rate is reduced (e.g., halved), system availability must decrease.
2. If a redundant edge is removed, system availability must not increase.
3. Units are consistent: both $\lambda$ and $\mu$ in $\mathrm{h}^{-1}$.

---

## 9. Frequent Point Deductions

1. Multiplying $duty$ directly onto $A$ (incorrect).
2. Treating parallel structure as an average (incorrect).
3. Reporting results without derivation.
4. Reporting "which is weak" without explaining "why".
5. Inconsistent convention (text says $\lambda_{eff}$, calculation uses $\lambda$).

---

## 10. Final Requirement

The goal is reproducible calculation, not formula memorization.  
Before submission, confirm:

- Can you compute one $A_i$ independently?
- Can you explain how $A_{sys}$ is obtained?
- Does Task 4 include cause + action + expected effect?

If all three are satisfied, this part is considered complete.
