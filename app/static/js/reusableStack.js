export function emailValidate(formData){
    const email = formData.emailField;
    const mailTest = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return mailTest.test(email);
 }


export function passwordValidate(formData){
    const pass = formData.passField;
    const passTest = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$/;
    // At least one lowercase, uppercase and digit and special character each. At least 8 characters long. 30 characters max.
    return passTest.test(pass)
 }