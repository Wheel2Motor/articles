function is_epoly_convex_hull m EPSILON:0.0001 = (
	local nverts = polyop.getNumVerts m
	local verts = polyop.getVerts m #{1..nverts}
	local normals = for i = 1 to (polyop.getNumFaces m) collect (polyop.getFaceNormal m i)
	local nedges = polyop.getNumEdges m
	for idxe = 1 to nedges do (
		local faces = (polyop.getFacesUsingEdge m idxe) as array
		-- Hole and Non-Manifest
		if faces.count != 2 do (
			return false
		)
		local f1 = faces[1]
		local f2 = faces[2]
		local nf1 = normalize normals[f1]
		local nf2 = normalize normals[f2]
		local d = dot nf1 nf2
		-- Acute angle
		if d < -EPSILON then (
			local vf1 = (polyop.getVertsUsingFace m f1) as array
			local vf2 = (polyop.getVertsUsingFace m f2) as array
			local cf1 = [0.0, 0.0, 0.0]
			local cf2 = [0.0, 0.0, 0.0]
			for i = 1 to vf1.count do (cf1 += verts[vf1[i]])
			cf1 /= vf1.count
			for i = 1 to vf2.count do (cf2 += verts[vf2[i]])
			cf2 /= vf2.count
			local ve = (polyop.getVertsUsingEdge m idxe) as array
			local lc = (verts[ve[1]] + verts[ve[2]]) / 2.0
			local cinner = cross nf1 nf2
			local coutter = cross (normalize (cf1 - lc)) (normalize (cf2 - lc))
			local r = dot cinner coutter
			if r > 0 do return false
		)
		-- Obtuse angle
		else if d > EPSILON do (
			local ne = normalize (nf1 + nf2)
			local vf1 = (polyop.getVertsUsingFace m f1) as array
			local vf2 = (polyop.getVertsUsingFace m f2) as array
			local cf1 = [0.0, 0.0, 0.0]
			local cf2 = [0.0, 0.0, 0.0]
			for i = 1 to vf1.count do (cf1 += verts[vf1[i]]); cf1 /= vf1.count
			for i = 1 to vf2.count do (cf2 += verts[vf2[i]]); cf2 /= vf2.count
			local ve = (polyop.getVertsUsingEdge m idxe) as array
			local lc = (verts[ve[1]] + verts[ve[2]]) / 2.0
			if dot ne (normalize (cf1 - lc)) > EPSILON do return false
		)
	)
	return true
)


for o in selection do (
	local r = is_epoly_convex_hull o
	if r then (print (o.name + " is Convex Hull"))
	else (print (o.name + " is not Convex Hull"))
)

