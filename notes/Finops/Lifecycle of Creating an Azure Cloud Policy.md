#finops #sop #arquitetura_solucoes #azure #cloudcomputing #cloud8 
## Prerequisites

You need [[Azure]] RBAC permissions in Azure Policy. The available permissions are:

- **Resource Policy Contributor:** include most Azure Policy Operations.
- **Owner:** has full rights.
- **Contributor:** access to all read operations and may trigger resource remediation. Can’t create or update definitions and assignments.
- **Reader:** access to all read operations.
- **User Access Administrator** to grant the managed identity on _deployIfNotExists_ or _modify_ assignments necessary permissions.

## Who needs to be involved:

- FinOps Practitioner will define the policies that will be established so that the environment can be configured to observe the best practices and requirements defined by other personas, ensuring that is achieved as collaborator.
- Engineering will create and implement the policies, ensuring that is achieved as driver.
- Product will be consulted about the impact of the new policies on cloud technology decisions, assuring that is achieved as decider.
- Security will be consulted about the impact of the new policies on the environment’s security, assuring that is achieved as contributor.
- ITFM will be consulted on the policies necessary to maintain control over costs, through the necessary definitions and constraints in the creation of new resources.

## Instructions for Running This Playbook

### **(1) Identify Stakeholders (30 Mins)**

The first step is to define who needs to be involved in the creation of a new policy. The FinOps Practitioner will define who are the key personas for defining the necessary policies, to present the risks and issues that arise from the policy, as well as justify its need.

**Example:** Creating a policy that restricts the regions where a particular resource can be created, such as databases and storage accounts. In this case, the legal department needs to be consulted about any obstacle to the selected region, to maintain compliance with regulatory requirements.

### **(2) Define the Policies (30 Min)**

Together with stakeholders, policies will be defined, and should consider the scope. Is highly recommended to define policies in broader scopes, to cover all child resources and facilitate the maintenance of the policy. In some cases, such as Azure, you can define a deletion sub scope, where the policy applied to a given scope in no longer applied.

Next, you need to define which business rules will be applied to non-compliant resources. They are:

- Notify a user
- Deny the change
- Register the change
- Change a resource before or after the trigger
- Deploy related compliant resources
- Block actions on resources

**Example:** The creation of a Azure Policy that prevents the creation of new resources without metadata. In this case, you can define a broad application scope, such as the subscription level, and then establish a sub scope to not apply the policy to Kubernetes resources.

![[Pasted image 20260414152149.png]]

### **(3) Develop and Implement the Policy (30 Mins)**

Document the policy that will be implemented, and which resources will be affected by it. Depending on the context, two documents can be used: **GMUD**, for changing cloud environments that are already established and will undergo changes; or **Implementation Plan**, in the case of cloud environments without previously defined policies.

Both must possess the following requirements: scope, responsibilities, standards, compliance requirements, monitoring and enforcement. Regarding the content: timeline, resources required, assignees, dependencies, and risks associated with implementation.

It is also important to document a **Test Plan**, which can be carried out through audit effects rather than actions on non-compliant resources, to validate results and ensure that policy definitions are correct.

**Example:** Using the example above, about creating resources without metadata, a test plan can use an audit effect instead of a deny action to validate that the scope has been applied.

![[Pasted image 20260414152215.png]]

A **Rollback Plan** should also be established defining the procedures to be followed in case the changes need to be reversed due to unforeseen problems or failures during implementation. It must contain the conditions for triggering the rollback, detailed steps to revert the changes, responsible and schedule.

### **(4) Review and Approval (30 Mins)**

After the implementation of the Policies, the review and approval of the changes can be followed through a **Post-Mortem Report** evaluating the success of the change after its implementation and documenting the lessons learned.

In this report, the impact of the established policies on environmental governance is analyzed, compared with the initial objectives, any problems encountered and their respective solutions, as well as possible optimization actions.

### **(5) Monitoring and Compliance (30 Mins)**

After the implementation of the Policies, conduct regular compliance monitoring, ensuring adherence to the established policies. For this you can use cloud-native tools for automatic checks, scheduled manual audits and **Compliance Reports** with the results obtained.

### **(6) Policy Review and Update (30 Mins)**

It’s necessary to review and update policies frequently, so that they remain relevant and effective. Changes in architecture, changes in regulatory requirements and the Compliance Reports themselves can demonstrate the need to change or revise policies that where once necessary. To do this, establish a **Policy Review Cycle**, which can be semiannual or annual, following the previous step-by-step for any change made.

### **(7) Decommissioning the Policy (30 Mins)**

In the same way that new regulatory requirements may arise, giving rise to the update of a policy, it may be necessary to delete a policy to compliance. In other cases, an established policy may conflict with another because they cover the same resources. In theses cases, if it’s necessary to exclude a policy, the procedure of a **GMUD** must be followed, obtaining express authorization from the stakeholders directly affected and communicating the effectiveness of the change.

## Outcomes and Indicators of Success

Once the environmental policies have been established, all stakeholders must be informed about the change in the environment that has taken place. When we talk about FinOps Policies, we expect that the new policies established and implemented will increase control over the resources created in the environment.

The idea is to optimize usage from implementation, avoiding the effort with corrective actions. The use of policy will ensure that engineering teams adhere to established standards from deployment to removal of a feature.

### Primary Outcomes of Running This Playbook

- **Improvement in cost allocation**: The use of policies can increase the maturity in Cost Allocation, through governance metadata standards that must be applied in the management of the cloud environment.
- **Increase control over the resources created**: The standards established by the policies optimize the use of the cloud, increasing control over the creation or alteration of resources, and in this way, avoiding the chaos generated by uncontrolled growth.
- **Usage Optimization**: Adopt policies to ensure that resources are utilized efficiently, minimizing the need for future corrective actions.
- **Compliance with Standards and Regulatory Requirements**: Ensure that all policies comply with regulatory requirements and internal standards, preventing legal or operational problems.

### Indicators of Success

- **Policy Compliance Rate**: Compliance Reports show that resources are adhering to established policies, reducing corrective interventions.
- **Reduction in the number of the amount of Non-Compliant resources**: Comparison of the amount of non-compliant resources at the beginning of the implementation and in the following evaluation sprints demonstrating a reduction in the occurrence of Non-Conformance.
- **Operational Efficiency**: Reduction of the time and effort required to manage and remediate resources due to the implementation of policies.
- **Stakeholder Satisfaction**: Feedback from stakeholders indicating that the policies implemented meet the needs and expectations regarding the governance of the environment.

### Exceptions and Considerations

As mentioned above, take into account that some Deny Policies can impact the maintenance of resource environments such as Kubernetes and Azure Virtual Desktop.