-- HR Help Desk Database Schema

-- Drop tables if they exist
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;

-- Create tickets table
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    employee_name VARCHAR(255) NOT NULL,
    employee_email VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Open',
    assigned_to VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create comments table
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    author VARCHAR(255) NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_category ON tickets(category);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_assigned_to ON tickets(assigned_to);
CREATE INDEX idx_comments_ticket_id ON comments(ticket_id);

-- Insert some sample data for testing
INSERT INTO tickets (employee_name, employee_email, category, priority, subject, description, status, assigned_to)
VALUES 
    ('John Doe', 'john.doe@company.com', 'Benefits', 'High', 'Health Insurance Question', 'I need help understanding my health insurance coverage options.', 'Open', NULL),
    ('Jane Smith', 'jane.smith@company.com', 'Payroll', 'Urgent', 'Missing Paycheck', 'I did not receive my paycheck for this month.', 'In Progress', 'Sarah Johnson'),
    ('Bob Wilson', 'bob.wilson@company.com', 'Time Off', 'Medium', 'Vacation Request', 'I would like to request time off for next month.', 'Open', NULL),
    ('Alice Brown', 'alice.brown@company.com', 'Onboarding', 'Low', 'New Hire Documentation', 'What documents do I need to submit as a new hire?', 'Resolved', 'Mike Davis'),
    ('Charlie Davis', 'charlie.davis@company.com', 'General', 'Medium', 'Office Access Card', 'My access card is not working properly.', 'Open', NULL);

-- Insert some sample comments
INSERT INTO comments (ticket_id, author, comment_text)
VALUES
    (2, 'Sarah Johnson', 'I am investigating this issue with the payroll department.'),
    (2, 'Sarah Johnson', 'The issue has been identified. Your paycheck will be processed today.'),
    (4, 'Mike Davis', 'Please submit your ID, social security card, and direct deposit form.'),
    (4, 'Alice Brown', 'Thank you! I have submitted all the documents.');
