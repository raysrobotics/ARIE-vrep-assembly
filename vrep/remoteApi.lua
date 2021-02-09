-- This is a customization script. It is intended to be used to customize a scene in
-- various ways, mainly when simulation is not running. When simulation is running,
-- do not use customization scripts, but rather child scripts if possible

-- Variable sim_call_type is handed over from the system

-- DO NOT WRITE CODE OUTSIDE OF THE if-then-end SECTIONS BELOW!! (unless the code is a function definition)
-- Add a dummy to the scene and attach a customization script to the dummy,
-- and then paste the following functions to the beginning of the script
-- outside the if-else statements.

loadModel_function=function(inInts,inFloats,inStrings,inBuffer)
	-- sim.importShape(0, "D:\\Projects\\3D models\\simbody_test\\hole_40_2.obj", 0, 0.0001, 1e-3)
	local handle = sim.importShape(inInts[1], inStrings[1], inInts[2], inFloats[1], inFloats[2])
	local result = sim.reorientShapeBoundingBox(handle, -1)
    return {handle},{},{},'' -- return the handle of the shape
end

setObjectName_function=function(inInts,inFloats,inStrings,inBuffer)
	-- sim.setObjectName(h_hole, "hole")
	local result = sim.setObjectName(inInts[1], inStrings[1])
	return {result},{},{},'' -- return the handle of the shape
end

checkCollision_function=function(inInts,inFloats,inStrings,inBuffer)
	-- sim.checkCollision(h_hole, h_peg)
	local isContact = sim.checkCollision(inInts[1], inInts[2])
	return {isContact},{},{},'' -- return the handle of the shape
end

setCameraFitToView_function=function(inInts,inFloats,inStrings,inBuffer)
	-- Set Peg and Hole fit to view
	local h_cam = sim.getObjectHandle("DefaultCamera")
	local result=sim.cameraFitToView(h_cam, {inInts[1], inInts[2]})
	return {result},{},{},'' -- return the handle of the shape
end

clearObjects_function=function(inInts,inFloats,inStrings,inBuffer)
	local objects=sim.getObjectsInTree(sim.handle_scene, sim.object_shape_type, 0)
	for i,v in pairs(objects) do
		--print( objects[i] )
        local name = sim.getObjectName(objects[i])
        local msg = string.format('Name: %s, Handle: %d', name, objects[i])
		--print(msg)
        print=printToConsole(msg)
		if (name == "peg" or name == "hole") then
			local result=sim.removeObject(objects[i])
            local msg = string.format('Removed - Name: %s, Handle: %d', name, objects[i])
            --print(msg)
            print=printToConsole(msg)
		end
	end
	return {},{},{},'' -- return the handle of the shape
end

findLowestPoint_function=function(inInts,inFloats,inStrings,inBuffer)
	-- inInts[1], inInts[2] : handle of peg and hole
	-- inFloats[1] : lower boundary of the search process
	-- inFloats[2] : precision of the downward process
	local h_peg, h_hol = inInts[1], inInts[2]

	local position = sim.getObjectPosition(h_peg,-1)
	local isContact = sim.checkCollision(h_hol, h_peg)

	while( isContact==0 and position[3]>inFloats[1] )
	do
		position=sim.getObjectPosition(h_peg,-1)
		position[3] = position[3]-inFloats[2]
		sim.setObjectPosition(h_peg,-1, position)

		isContact = sim.checkCollision(h_hol, h_peg)
	end

	if (isContact==1) then
		return {0},{position[1],position[2],position[3]},{},'' -- return the handle of the shape
	end

	if (position[3]<=inFloats[1]) then
		return {-1},{position[1],position[2]},{},'' -- return the handle of the shape
	end
end

findLowestPoint=function(h_peg, h_hol, x, y, z_init, downward_depth, downward_precision )
	if (nil == x and nil == y) then
		local pos = sim.getObjectPosition(h_peg, -1)
		x = pos[1]
		y = pos[2]
	end

	if nil == z_init then
        z_init = 0.1
	end
	if nil == downward_depth then
        downward_depth = -0.08
	end
	if nil == downward_precision then
        downward_precision = 1e-4
    end

	-- Set peg to *position*
	local position = {x, y, z_init}
	sim.setObjectPosition(h_peg, -1, position)

	-- Check if the peg and hold collide at the initial position
    -- If yes, move the peg up along z-axis so that they will not
    -- collide at the inital position
	local isContact = sim.checkCollision(h_hol, h_peg)
	while( isContact==1 )
	do
		position=sim.getObjectPosition(h_peg, -1)
		position[3] = position[3]+downward_precision*5
		sim.setObjectPosition(h_peg, -1, position)

		isContact = sim.checkCollision(h_hol, h_peg)
	end

    -- While the peg and hole do not collide, and the peg's z coordinate
    -- is not lower than input parameter --depth (default: -0.08), then
    -- move the peg downwards along z-axis
	while( isContact==0 and position[3]>downward_depth )
	do
		position = sim.getObjectPosition(h_peg,-1)
		position[3] = position[3]-downward_precision
		sim.setObjectPosition(h_peg, -1, position)

		isContact = sim.checkCollision(h_hol, h_peg)
	end

	if (isContact==1) then
		return 0, {position[1],position[2],position[3]}
	end

	if (position[3]<=downward_depth) then
		return -1, {position[1],position[2]}
	end
end

findLowestPoint2_function=function(inInts,inFloats,inStrings,inBuffer)
	-- inInts[1], inInts[2] : handle of peg and hole
	-- inFloats[1] : lower boundary of the search process
	-- inFloats[2] : precision of the downward process
	-- inFloats[3] : Initial height of the peg in downward process
	local h_peg, h_hol = inInts[1], inInts[2]
	local x, y, z_init = inFloats[3], inFloats[4], inFloats[5]
	local downward_depth = inFloats[1]
	local downward_precision = inFloats[2]

    local retFlag, position = findLowestPoint(h_peg, h_hol, x, y, z_init, downward_depth, downward_precision)

	if (retFlag==0) then
    -- If the peg and hole collide, output:
    -- retInts[0] == 0
    -- retFloats = {x, y, z}
		return {0},{position[1],position[2],position[3]},{},'' -- return the handle of the shape
	else
	-- If the peg and hole do not collide, output:
    -- retInts[0] == -1
    -- retFloats = {x, y}
		return {-1},{position[1],position[2]},{},''
	end

end

-- findLowestPoint2_function=function(inInts,inFloats,inStrings,inBuffer)
-- 	-- inInts[1], inInts[2] : handle of peg and hole
-- 	-- inFloats[1] : lower boundary of the search process
-- 	-- inFloats[2] : precision of the downward process
-- 	-- inFloats[3] : Initial height of the peg in downward process
-- 	local h_peg, h_hol = inInts[1], inInts[2]
-- 	local x, y, z_init = inFloats[3], inFloats[4], inFloats[5]

--     -- Set peg to *position*
-- 	local position = {x, y, z_init}
--     sim.setObjectPosition(h_peg, -1, position)

--     -- Check if the peg and hold collide at the initial position
--     -- If yes, move the peg up along z-axis so that they will not
--     -- collide at the inital position
-- 	local isContact = sim.checkCollision(h_hol, h_peg)
-- 	while( isContact==1)
-- 	do
-- 		position=sim.getObjectPosition(h_peg,-1)
-- 		position[3] = position[3]+inFloats[2]*5
-- 		sim.setObjectPosition(h_peg,-1, position)

-- 		isContact = sim.checkCollision(h_hol, h_peg)
-- 	end

--     -- While the peg and hole do not collide, and the peg's z coordinate
--     -- is not lower than input parameter --depth (default: -0.08), then
--     -- move the peg downwards along z-axis
-- 	while( isContact==0 and position[3]>inFloats[1] )
-- 	do
-- 		position=sim.getObjectPosition(h_peg,-1)
-- 		position[3] = position[3]-inFloats[2]
-- 		sim.setObjectPosition(h_peg,-1, position)

-- 		isContact = sim.checkCollision(h_hol, h_peg)
-- 	end

--     -- If the peg and hole collide, output:
--     -- retInts[0] == 0
--     -- retFloats = {x, y, z}
-- 	if (isContact==1) then
-- 		return {0},{position[1],position[2],position[3]},{},'' -- return the handle of the shape
--     end

--     -- If the peg and hole do not collide, output:
--     -- retInts[0] == -1
--     -- retFloats = {x, y}
-- 	if (position[3]<=inFloats[1]) then
-- 		return {-1},{position[1],position[2]},{},'' -- return the handle of the shape
-- 	end
-- end

findARIE_function=function(inInts,inFloats,inStrings,inBuffer)
	local h_peg, h_hol = inInts[1], inInts[2]
	local x_start, x_delta, x_end = inFloats[1], inFloats[2], inFloats[3]
	local y_start, y_delta, y_end = inFloats[4], inFloats[5], inFloats[6]
	local z_init = inFloats[7]
	local downward_depth, downward_precision = inFloats[8], inFloats[9]

	local timestamp=os.date("%Y-%m-%d-%H%M")
	local filename = "results" .. timestamp .. ".csv"
	h_file = io.open(filename, "w+")
	io.output(h_file)

	local prog_i = 0
	for x = x_start, x_end, x_delta do

		local prog_now = (x-x_start)/(x_end-x_start);
		if (prog_now - prog_i >= 0.01) then
			local msg = string.format('%s - Progress: %.2f%%\n', os.date(), prog_now*100)
			sim.addStatusbarMessage(msg)
			print(msg)
			prog_i = prog_now;
		end

		for y = y_start, y_end, y_delta do
			retInts, retFloats, retStrings, retBuffer = findLowestPoint2_function({h_peg, h_hol}, {downward_depth, downward_precision, x, y, z_init}, {}, {})
			if (retInts[1] == 0) then
				io.write(string.format("%f, %f, %f\n", retFloats[1], retFloats[2], retFloats[3]))
			else
				if (retInts[1] == -1) then
					io.write(string.format("%f, %f, Inf\n", retFloats[1], retFloats[2]))
				else
					io.write(string.format("Inf, Inf, Inf\n"))
				end
			end
		end
	end
	io.close(h_file)
	sim.addStatusbarMessage("file saved!\n") -- print to the statusbar
	print("file saved!\n") -- print to the console
	return {},{},{},'' -- return the handle of the shape
end



if (sim_call_type==sim.syscb_init) then
    -- this is called just after this script was created (or reinitialized)
    -- Do some initialization here

    -- By default we disable customization script execution during simulation, in order
    -- to run simulations faster:
    sim.setScriptAttribute(sim.handle_self,sim.customizationscriptattribute_activeduringsimulation,false)
end

if (sim_call_type==sim.syscb_nonsimulation) then
    -- This is called on a regular basis when simulation is not running.
    -- This is where you would typically write the main code of
    -- a customization script
end

if (sim_call_type==sim.syscb_beforesimulation) then
    -- This is called just before a simulation starts
end

if (sim_call_type==sim.syscb_actuation) then
    -- This is called by default from the main script, in the "actuation" phase.
    -- but only if you have previously not disabled this script to be active during
    -- simulation (see the script's initialization code above)
end

if (sim_call_type==sim.syscb_sensing) then
    -- This is called by default from the main script, in the "sensing" phase,
    -- but only if you have previously not disabled this script to be active during
    -- simulation (see the script's initialization code above)
end

if (sim_call_type==sim.syscb_suspend) then
    -- This is called just after entering simulation pause
end

if (sim_call_type==sim.syscb_suspended) then
    -- This is called on a regular basis when simulation is paused
end

if (sim_call_type==sim.syscb_resume) then
    -- This is called just before leaving simulation pause
end

if (sim_call_type==sim.syscb_aftersimulation) then
    -- This is called just after a simulation ended
end

if (sim_call_type==sim.syscb_beforeinstanceswitch) then
    -- This is called just before an instance switch (switch to another scene)
end

if (sim_call_type==sim.syscb_afterinstanceswitch) then
    -- This is called just after an instance switch (switch to another scene)
end

if (sim_call_type==sim.syscb_cleanup) then
    -- this is called just before this script gets destroyed (or reinitialized)
    -- Do some clean-up here
end
