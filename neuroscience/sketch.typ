
// ==========================================
// TEMPLATE DEFINITION
// ==========================================
#let assignment(
  title: "",
  course: "",
  author: "",
  ta: "",
  date: datetime.today().display(),
  body
) = {
  // Document Metadata
  set document(author: author, title: title)
  
  // Page Configuration (Updated to modern `context` syntax)
  set page(
    paper: "a4",
    margin: (x: .9in, y: 0.7in),
    header: context {
      if counter(page).get().first() > 1 {
        align(right)[#text(size: 8pt, fill: luma(120))[#course -- #title]]
      }
    },
    numbering: "1",
  )

  // Global Typography
  set text(font: "New Computer Modern", size: 15pt)
  set par(justify: true, leading: 0.8em)
  show heading: set block(above: 1.5em, below: 1em)
  set math.equation()

  // Title Block (Fixed argument syntax)
  align(center)[
    #block(text(weight: "bold", size: 1.5em)[#title])
    #v(0.5em)
    #grid(
      columns: (1fr, 1fr),
      align: (center, center),
      [*Author:* #author ],
      [ *Date:* #date]
    )
  ]
  
  // Minimalist Divider
  v(1em)
  line(length: 100%, stroke: 1pt + luma(200))
  v(1.5em)

  body
}

// ==========================================
// CUSTOM ENVIRONMENTS
// ==========================================
#let problem(num, body) = block(above: 1.5em, below: 1.5em)[
  -- *Problem #num:* \
  #body
]

#let solution(body) = block(above: 1em, below: 1.5em)[
  ----- *_Solution:_* \
  #body
]

// ==========================================
// DOCUMENT CONTENT
// ==========================================
#show: assignment.with(
  title: "Neuroscience notes",
  author: "Rosh Guadiana",
)


+ The bioelectricity
+ History of Luigi Galvani and the nerve of the frog 1771.
== What is a neuron?
  - A neuron in resting potential
 How do same and opposite charges interact?
What is voltage? How is voltage related to electrical potential? 
\
Comparison to the mechanical potential energy
  - electrostatic force description
In neuroscience, the relevant points in space are the inside and the outside of a cell, which are separated by a membrane that is impermeable to charged particles. Ions cannot flow across this membrane without the help of channels or pumps.
\ neuroscientists always use the outside of the cell as the ‘ground’

== Resting potential

Membrane potentials when the neurons are at rest. 
Neurons are able to send signals through the use of electricity, and we see that neurons themselves are electrically charged.

\ the lipid membrane of neurons separates solutions of charged particles, such as K+ and Na+ ions, and this separation creates a difference in potential energy across the lipid membrane. 

In neurons that are not sending or receiving signals, this potential difference is called the ‘resting potential.’

Both inside and outside of the neuron, ions and other particles exist in an aqueous solution and are able to move around. There are many forces that can guide their behavior, two of which are important to us: the diffusive and electrostatic forces. 

It’s important for us to understand how these forces affect the movement of charged particles such as K+ and Na+ ions, since the movement of these ions across the membrane of a neuron can change its membrane potential. Both of these forces will be important for us when understanding how the resting potential is established. By the end of this video, you should be able to answer the following questions:
